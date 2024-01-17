"""
.. module:: constants.status.

    :synopsis: Defines request statuses used throughout the application
"""

NDA = 'Needs Division Approval'
NCA = 'Needs Commissioner Approval'
APR = 'Approved - Pending'
DEN = 'Denied'
RES = 'Resolved'
HOLD = 'Hold'

STATUS_DROPDOWN = [
    ("New", "New"),
    ("Awaiting Admin Approval", "Awaiting Admin Approval"),
    ("Awaiting Division Approval", "Awaiting Division Approval"),
    ("Awaiting Commissioner Approval", "Awaiting Commissioner Approval"),
    ("Approved", "Approved"),
    ("Denied", "Denied"),
    ("Order Placed", "Order Placed"),
    ("In Transit", "In Transit"),
    ("Backorder", "Backorder"),
    ("Completed", "Completed"),
]
