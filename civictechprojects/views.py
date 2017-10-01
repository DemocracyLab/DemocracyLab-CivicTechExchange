from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .serializers import ProjectSerializer

from pprint import pprint

from .models import Project as realProject
from democracylab.models import get_request_contributor

from .forms import ProjectCreationForm


class Tag:
    pass

def tag(name):
    res = Tag()
    res.tag_name = name.lower().replace(' ', '_')
    res.display_name = name
    return res

def tags(*tags):
    return [tag(t) for t in tags]
PROJECT_KINDS = tags(
    '1st Amendment',
    '2nd Amendment',
    'Cultural Issues',
    'Economy',
    'Education',
    'Environment',
    'Health Care',
    'Homelessness',
    'Housing',
    'Immigration',
    'International Issues',
    'National Security',
    'Political Reform',
    'Public Safety',
    'Social Justice',
    'Taxes',
    'Transportation',
    'Other'
)

SKILL_KINDS = tags(
    'Accounting',
    'Back-End Development',
    'Business Strategy',
    'Copywriting',
    'Data Science',
    'Data Visualization',
    'Database Architecture',
    'Front-End Development',
    'Fundraising',
    'Graphic Design',
    'Legal Services',
    'Project Management',
    'Research',
    'UI Design',
    'UX Design',
    'Other'
)

TECHNOLOGIES = tags(
    'Python',
    'C',
    'Java',
    'C++',
    'C#,'
    'R',
    'JavaScript',
    'PHP',
    'Go',
    'Swift'
)

STATUS = tags(
    'Updated',
    'Active',
    'Less Active',
    'Dormant',
    'Abandoned'
)

STAGES = tags(
    'New Idea',
    'Research',
    'Requirements Gathering and Analysis',
    'Planning',
    'Design',
    'Development',
    'Release',
    'Iteration',
)

PROJECT_TYPES = tags(
    'Government Efficiency',
    'Civic Engagement',
    'Community Organizing',
    'Infrastructure'
)

# PROJECT_SUBTYPES = tags(
#     ''
# )

def to_columns(items, count = 3):
    res = []
    for i in range(count):
        res.append([])
    cur = 0
    for item in items:
        res[cur % count].append(item)
        cur+=1
    return res


def project_signup(request):
    if request.method == 'POST':
        form = ProjectCreationForm(request.POST)
        form.is_valid()
        # pprint(vars(request._post))
        # TODO: Form validation
        project = realProject(
            project_creator=get_request_contributor(request),
            project_name=form.cleaned_data.get('project_name'),
            project_url=form.cleaned_data.get('project_url'),
            project_description=form.cleaned_data.get('project_description'),
            project_tags=form.cleaned_data.get('project_tags'),
        )
        project.save()
        return redirect('/')
    else:
        form = ProjectCreationForm()

    template = loader.get_template('project_signup.html')
    context = {'form': form,
        'skills':to_columns(SKILL_KINDS),
        'projects':to_columns(PROJECT_KINDS),
        'technologies':TECHNOLOGIES,
        'project_types':PROJECT_TYPES,
        'stages':STAGES,
        'status':STATUS
    }
    return HttpResponse(template.render(context, request))

class Project:
    def __init__(self, image_url, name, description, status):
        self.image_url = image_url
        self.name = name
        self.description = description
        self.status = status

PROJECTS = [
    Project('/static/images/projectPlaceholder.png','DemocracyLab', 'We support technology for the public good by connecting passionate people with impactful projects.', 'Accepting Contributions'),
    Project('/static/images/projectPlaceholder.png','Redesigning Washington Legislative Web Services', 'Port information from WA legislative services website into a more user-friendly format and add more data to encourage civic engagement.', 'Accepting Contributions'),
    Project('/static/images/projectPlaceholder.png','SDOT', 'Bringing digital equity to public transportation', 'Accepting Contributions'),
    Project('/static/images/projectPlaceholder.png','Haskell Bindings to the Socrata Open Data API', 'Creating libraries for Haskell bindings to the Socrata Open Data API (SODA). ', 'Accepting Contributions'),
    Project('/static/images/projectPlaceholder.png','Using AI and Satellite Imagery to Protect Our Wetlands', 'Using AI and satellite imagery to help track and call attention to major changes made to our environment.', 'Accepting Contributions'),
    Project('/static/images/projectPlaceholder.png','DESC Project Brainstorming', 'Forming ideas for a technology project to benefit DESC, the largest homeless agency in Seattle.', 'Accepting Contributions'),
    Project('/static/images/projectPlaceholder.png','Civic User Testing Group', 'Giving Seattle residents a way to participate in civic tech by getting paid to test and provide user feedback on civic tech projects. ', 'Accepting Contributions'),
    Project('/static/images/projectPlaceholder.png','DemocracyLab', 'We support technology for the public good by connecting passionate people with impactful projects.', 'Accepting Contributions'),
]

def index(request):
    template = loader.get_template('index.html')
    print(to_columns(PROJECTS,4))
    context = {'projects':to_columns(PROJECTS,2)}
    return HttpResponse(template.render(context, request))



def home(request):
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))


def projects_list(request):
    if request.method == 'GET':
        projects = Project.objects.order_by('-project_name')
    serializer = ProjectSerializer(projects, many=True)
    return JsonResponse(serializer.data, safe=False)
