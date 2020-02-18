from typing import List


class Person:
    def __init__(self, name: str):
        self.name = name


class SHG:
    def __init__(self, shg_name: str, people: List[Person]):
        self.shg_name = shg_name
        self.people = people


shg = SHG(
    shg_name=input.get("shg_name"),
    people=[
        Person(name="foo")
    ]

)


@app.route("/store")
def store_shg():
    args.get()
    shg = // create
    object
    shg.save()


shg.save()