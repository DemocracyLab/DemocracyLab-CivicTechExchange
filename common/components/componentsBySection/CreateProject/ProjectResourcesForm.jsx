// @flow

import React from "react";
import DjangoCSRFToken from "django-react-csrftoken";
import type { ProjectDetailsAPIData } from "../../utils/ProjectAPIUtils.js";
import { LinkVisibility, LinkInfo } from "../../forms/LinkInfo.jsx";
import type { FileInfo } from "../../common/FileInfo.jsx";
import LinkList, { NewLinkInfo } from "../../forms/LinkList.jsx";
import FileUploadList from "../../forms/FileUploadList.jsx";
import formHelper, { FormPropsBase, FormStateBase } from "../../utils/forms.js";
import FormValidation from "../../forms/FormValidation.jsx";
import type { Validator } from "../../forms/FormValidation.jsx";
import { OnReadySubmitFunc } from "./ProjectFormCommon.jsx";
import { DefaultLinkDisplayConfigurations } from "../../constants/LinkConstants.js";
import HiddenFormFields from "../../forms/HiddenFormFields.jsx";
import url from "../../utils/url.js";
import _ from "lodash";

type FormFields = {|
  project_links: Array<LinkInfo>,
  project_files: Array<FileInfo>,
  link_coderepo: ?string,
  link_messaging: ?string,
  link_projmanage: ?string,
  link_filerepo: ?string,
|};

type Props = {|
  project: ?ProjectDetailsAPIData,
  readyForSubmit: OnReadySubmitFunc,
|} & FormPropsBase<FormFields>;

type State = {| linkDict: Dictionary<LinkInfo> |} & FormStateBase<FormFields>;

const resourceLinks: $ReadOnlyArray<string> = [
  "link_coderepo",
  "link_messaging",
  "link_projmanage",
  "link_filerepo",
];

/**
 * Encapsulates form for Project Resources section
 */
class ProjectResourcesForm extends React.PureComponent<Props, State> {
  constructor(props: Props): void {
    super(props);
    const project: ProjectDetailsAPIData = props.project;
    const formFields: FormFields = {
      project_links: project ? project.project_links : [],
      project_files: project ? project.project_files : [],
      link_coderepo: "",
      link_messaging: "",
      link_projmanage: "",
      link_filerepo: "",
    };
    // TODO: Validate every field
    const validations: $ReadOnlyArray<Validator<FormFields>> = [
      {
        checkFunc: (formFields: FormFields) =>
          url.isEmptyStringOrValidUrl(formFields["link_coderepo"]),
        errorMessage: "Please enter valid URL for code repository website.",
      },
      {
        checkFunc: (formFields: FormFields) =>
          url.isEmptyStringOrValidUrl(formFields["link_messaging"]),
        errorMessage: "Please enter valid URL for messaging website.",
      },
      {
        checkFunc: (formFields: FormFields) =>
          url.isEmptyStringOrValidUrl(formFields["link_projmanage"]),
        errorMessage: "Please enter valid URL for project management website.",
      },
      {
        checkFunc: (formFields: FormFields) =>
          url.isEmptyStringOrValidUrl(formFields["link_filerepo"]),
        errorMessage: "Please enter valid URL for file repository website.",
      },
    ];
    const formIsValid: boolean = FormValidation.isValid(
      formFields,
      validations
    );
    this.state = {
      formFields: formFields,
      formIsValid: formIsValid,
      validations: validations,
      linkDict: this.generateLinkDict(props),
    };
    //this will set formFields.project_links and formFields.links_*
    this.filterSpecificLinks(_.cloneDeep(project.project_links));
    this.form = formHelper.setup();
    props.readyForSubmit(formIsValid, this.onSubmit.bind(this));
  }

  componentDidMount() {
    this.form.doValidation.bind(this)();
  }

  generateLinkKey(link: NewLinkInfo): string {
    if (_.includes(resourceLinks, link.linkName)) {
      return link.linkName;
    } else {
      const id: string = link.tempId || link.id;
      return link.linkName + id;
    }
  }

  generateLinkDict(props: Props): Dictionary<LinkInfo> {
    const linkDict: Dictionary<LinkInfo> = _.mapKeys(
      props.project.project_links,
      this.generateLinkKey
    );
    resourceLinks.forEach((linkType: string) => {
      if (!(linkType in linkDict)) {
        linkDict[linkType] = {
          linkName: linkType,
          visibility: LinkVisibility.PUBLIC,
          linkUrl: "",
        };
      }
    });

    return linkDict;
  }

  onValidationCheck(formIsValid: boolean): void {
    if (formIsValid !== this.state.formIsValid) {
      this.setState({ formIsValid });
      this.props.readyForSubmit(formIsValid, this.onSubmit.bind(this));
    }
  }

  // TODO: Put common code used between EditProjectsForm in a common place
  onSubmit(submitFunc: Function): void {
    //Sanitize project url if necessary
    if (this.state.formFields.project_url) {
      this.state.formFields.project_url = url.appendHttpIfMissingProtocol(
        this.state.formFields.project_url
      );
    }
    // TODO: Do we need this?
    let formFields = this.state.formFields;
    formFields.project_links = _.values(this.state.linkDict).filter(
      (link: LinkInfo) => !_.isEmpty(link.linkUrl)
    );
    this.setState({ formFields: formFields }, submitFunc);
    this.forceUpdate();
  }

  filterSpecificLinks(array) {
    //this function updates the entire state.formFields object at once
    let specificLinks = _.remove(array, function(n) {
      return n.linkName in DefaultLinkDisplayConfigurations;
    });
    //copy the formFields state to work with
    let linkState = this.state.formFields;
    //pull out the link_ item key:values and append to state copy
    specificLinks.forEach(function(item) {
      linkState[item.linkName] = item.linkUrl;
    });
    //add the other links to state copy
    linkState["project_links"] = array;

    //TODO: see if there's a way to do this without the forceUpdate - passing by reference problem?
    this.setState({ formFields: linkState });
    this.forceUpdate();
  }

  onAddLink(link: NewLinkInfo): void {
    const key: string = this.generateLinkKey(link);
    const linkDict: Dictionary<NewLinkInfo> = _.clone(this.state.linkDict);
    linkDict[key] = link;
    this.setState({ linkDict: linkDict });
  }

  onChangeLink(
    linkKey: string,
    input: SyntheticInputEvent<HTMLInputElement>
  ): void {
    this.state.linkDict[linkKey].linkUrl = input.target.value;
    this.form.onInput.call(this, linkKey, input);
    // this.forceUpdate();
  }

  render(): React$Node {
    return (
      <div className="EditProjectForm-root">
        <DjangoCSRFToken />

        <HiddenFormFields
          sourceDict={{
            project_links: JSON.stringify(
              this.state.formFields.project_links || []
            ),
          }}
        />

        <div className="form-group">
          <LinkList
            elementid="resource_links"
            title="Project Resources"
            subheader="Paste the links to your internal collaboration tools"
            links={this.state.formFields.project_links}
            linkDict={this.state.linkDict}
            linkOrdering={resourceLinks}
            onAddLink={this.onAddLink.bind(this)}
            onChangeLink={this.onChangeLink.bind(this)}
          />
        </div>

        <div className="form-group">
          <FileUploadList
            elementid="project_files"
            title="Project Files"
            files={this.state.formFields.project_files}
            onChange={this.form.onFormChange.bind(this)}
          />
        </div>

        <FormValidation
          validations={this.state.validations}
          onValidationCheck={this.onValidationCheck.bind(this)}
          formState={this.state.formFields}
        />
      </div>
    );
  }
}

export default ProjectResourcesForm;
