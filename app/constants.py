"""
.. module: constants

    :synopsis: Defines constants used throughout the application.
"""

statuses = {
    1: 'Submitted',
    2: 'Needs Division Approval',
    3: 'Needs Commissioner Approval',
    4: 'Pending - Approved',
    5: 'Denied',
    6: 'Resolved',
    7: 'Hold'
}

divisions = {
    'MRMD': 'Records Management',
    'ARC': 'Archives',
    'GRA': 'Grants',
    'LIB': 'Library',
    'EXEC': 'Executive',
    'MIS': 'MIS/Web',
    'ADM': 'Administration'
}
