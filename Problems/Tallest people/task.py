def tallest_people(**kwargs):
    tallest = max(kwargs.values())
    tallest_person = [person for person in kwargs if kwargs[person] == tallest]
    for person in sorted(tallest_person):
        print('{} : {}'.format(person, tallest))
