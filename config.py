import yaml


def get_config(l_key):
    with open("config.yaml", "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        l_value = data[l_key]
    return l_value