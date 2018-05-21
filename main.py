from itertools import combinations
from random import sample, shuffle
import asyncio


class Member:
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    played = won = lost = drew = stat = 0

    def win(self, stat):
        self.won += 1
        self.played += 1
        self.stat += stat

    def lose(self, stat):
        self.lost += 1
        self.played += 1
        self.stat += stat

    def draw(self, stat):
        self.drew += 1
        self.played += 1
        self.stat += stat


class Fixture:

    def __init__(self, pair):
        self.member1 = pair[0]
        self.member2 = pair[1]

    def __str__(self):
        return str(self.member1) + ' v/s ' + str(self.member2)

    winner = stat = 0


class Group:

    def __init__(self, group, name):
        self.members = group
        self.name = "Group " + name
        self.fixtures = None

    def __getitem__(self, i):
        return self.members[i]

    def __len__(self):
        return len(self.members)

    def set_fixtures(self, fixtures):
        self.fixtures = fixtures


class League:

    def __init__(self, groups_tuple):
        self.groups = list(groups_tuple)

    def __getitem__(self, i):
        return self.groups[i]


def get_sizes():
    while 1:
        try:
            group_number = int(input("Enter number of groups: "))
        except ValueError:
            print("Enter an integer.")
            continue
        if group_number < 1:
            print("Minumum number of groups is 1")
            continue
        if group_number > 64:
            print("Maximum number of groups is 64")
            continue
        break
    while 1:
        try:
            group_size = int(input("Enter size of each group: "))
        except ValueError:
            print("Enter an integer.")
            continue
        if group_size < 3:
            print("Minumum size of a group is 3")
            continue
        if group_size > 64:
            print("Maximum size of a group is 64")
            continue
        break
    return group_number, group_size


def get_members(size):
    members_list = []
    for i in range(size):
        members_list.append(Member("Player%d"%i))
    return tuple(members_list)


def make_groups(members_tuple, group_number, group_size):
    members_list = list(members_tuple)
    groups_list = []
    name = 65
    while members_list:
        group = sample(members_list, group_size)
        for i in group:
            members_list.remove(i)
        groups_list.append(Group(group, chr(name)))
        name += 1
    return tuple(groups_list)


def check_gap(group_fixtures):
    for i in range(len(group_fixtures) - 1):
        if len(set(group_fixtures[i] + group_fixtures[i+1])) != 4:
            return 0
    return 1


def small_check_gap(group_fixtures):
    for i in (0, 2, 4):
        if len(set(group_fixtures[i] + group_fixtures[i+1])) != 4:
            return 0
    return 1


async def make_fixtures(group):
    group_fixtures = list(combinations(group, 2))
    while not check_gap(group_fixtures) and len(group) > 4:
        shuffle(group_fixtures)
    while not small_check_gap(group_fixtures) and len(group) == 4:
        shuffle(group_fixtures)
    group_fixtures = map(Fixture, group_fixtures)
    group.set_fixtures(group_fixtures)


group_number, group_size = get_sizes()
members_tuple = get_members(group_number * group_size)
groups_tuple = make_groups(members_tuple, group_number, group_size)
#make_fixtures(groups_tuple)

async def call_function(groups_tuple):
    threadlist = [make_fixtures(group) for group in groups_tuple]
    await asyncio.gather(*threadlist)

event = asyncio.get_event_loop()
event.run_until_complete(call_function(groups_tuple))

for group in groups_tuple:
    print('\n' + group.name)
    for member in group:
        print(member)

for group in groups_tuple:
    print('\n' + group.name)
    for match in group.fixtures:
        print(match)
