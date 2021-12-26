from datetime import date


def save_protocol(data):
    """
    saves the created protocol
    """
    print("creating protocol...")
    file_name = 'Brauvorgang_'+date.today().strftime('%Y-%m-%d')+".pdf"
    hallo = open(file_name, "w")
    f = open(file_name, "w")
    f.write(data)
    f.close()
