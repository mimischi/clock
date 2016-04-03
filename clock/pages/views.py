from django.shortcuts import render

from clock.shifts.forms import QuickActionForm
from clock.shifts.utils import get_all_contracts, get_current_shift, \
    get_default_contract

# from config.settings.common import GIT_STATUS, GIT_REVISION_HASH, GIT_COMMIT_TIMESTAMP


def home(request):
    """
    Just render the home screen.
    """
    context = {}

    template_to_render = 'pages/frontend/index.html'

    if request.user.is_authenticated():
        context['all_contracts'] = get_all_contracts(request.user)
        context['default_contract'] = get_default_contract(request.user)
        # context['git_revision_hash'] = GIT_REVISION_HASH
        # context['git_commit_timestamp'] = GIT_COMMIT_TIMESTAMP
        template_to_render = 'pages/backend/index.html'

        # Initialize the QuickActionForm
        context['form'] = QuickActionForm(user=request.user)

        # Get the current shift to display the possible quick-actions.
        shift = get_current_shift(request.user.id)

        # Check if we have a current shift. Either fill the data for
        # the template or use an empty context variable.
        if shift:
            context['shift_closed'] = bool(shift)
            context['shift_paused'] = shift.is_paused

            # Delete the 'all_contracts' key from the context dict,
            # so we can hide the <select>-element in the template.
            del context['all_contracts']

    # Render the template
    return render(request, template_to_render, context)
