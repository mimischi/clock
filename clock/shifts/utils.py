from datetime import date

from django.core.exceptions import ValidationError

from clock.contracts.models import Contract
from clock.shifts.models import Shift


def get_current_shift(user):
    entries = Shift.objects.filter(employee=user, shift_finished__isnull=True)

    if not entries.exists():
        return None
    # if entries.count() > 1:
    #     raise ActiveEntryError('Only one active entry is allowed.')
    return entries[0]


def get_all_contracts(user):
    """
    Returns all contracts an user has signed.
    """
    return user.contract_set.all()


def get_default_contract(user):
    """
    Returns the default institute of the user.
        - If the user has any finished shifts, then return the contract
          of the last finished shift.
        - If no shifts were finished yet, but the user has defined contracts,
          return the contract that was added first.
        - If no contracts are defined, then return the NoneObject as default
    """
    # Filter all shifts (finished or not) from the current user
    finished_shifts = Shift.objects.filter(employee=user)

    # If the user has shifts
    if finished_shifts:
        # Are there any shifts finished for a non-default contract?
        if finished_shifts[0].contract is not None:
            # Return the contract of the latest shift
            return finished_shifts[0].contract.department

    # Return NoneObject for the default None-contract
    return None


def get_last_shifts(user, count=5):
    finished_shifts = Shift.objects.filter(employee=user, shift_finished__isnull=False)[:count]

    if not finished_shifts:
        return None

    return finished_shifts


def get_all_shifts(user):
    shifts = Shift.objects.filter(employee=user, shift_finished__isnull=False)

    months_with_shifts = []

    for shift in shifts:
        year = shift.shift_started.year
        month = shift.shift_started.month
        shift_dict = {'year': year, 'month': month}

        if shift_dict not in months_with_shifts:
            months_with_shifts.append(shift_dict)

    return months_with_shifts


def month_with_shift(user, month, year, mode):
    all_shifts = get_all_shifts(user)

    curr_month = month
    curr_year = year

    if mode == "prev":
        if 0 < month < 2:
            month = 12
            year -= 1
        else:
            month -= 1
    elif mode == "next":
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
    f = -1
    lookup_month = ''
    while f < 0:
        for index, shift_month in enumerate(all_shifts):
            if shift_month.get('month') == month and shift_month.get('year') == year:
                f = index
                lookup_month = date(year, month, 1)
                break

        for index, shift_month in enumerate(all_shifts):
            searchDate = date(shift_month.get('year'), shift_month.get('month'), 1)
            if mode == "prev":
                if searchDate < date(curr_year, curr_month, 1):
                    lookup_month = searchDate
                    f = index
                    break
            elif mode == "next":
                if searchDate > date(curr_year, curr_month, 1):
                    lookup_month = searchDate
                    f = index
                    break
        if f < 0:
            return None
        else:
            break
    return lookup_month


def shifts_in_month(user, month, year, mode):
    if mode == "prev":
        if 0 < month < 2:
            month = 12
            year -= 1
        else:
            month -= 1
    elif mode == "next":
        if month == 12:
            month = 01
            year += 1
        else:
            month += 1
    else:
        raise ValidationError('You\'re not using this method correctly!')

    shifts = Shift.objects.filter(employee=user,
                                  shift_started__year=year,
                                  shift_started__month=month,
                                  shift_finished__isnull=False).exists()

    if shifts:
        return True

    return False
