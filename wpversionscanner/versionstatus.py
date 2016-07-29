
UPDATE_STATUS = ["SEVERE", "MEDIUM", "GOOD"]
COLOURS = ['\033[91m', '\033[93m', '\033[92m']


def get_status(status):
    return UPDATE_STATUS[status]

def get_colour(status):
    if status == "END":
        return '\033[0m'
    else:
        return COLOURS[status]
