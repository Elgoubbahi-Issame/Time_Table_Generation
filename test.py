import mysql.connector
import prettytable as prettytable
import random as rnd
POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05


class Instructor:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    def get_id(self): return self._id
    def get_name(self): return self._name
    def __str__(self): return self._name


class Room:
    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity

    def get_number(self): return self._number
    def get_seatingCapacity(self): return self._seatingCapacity


class MeetingTime:
    def __init__(self, id, time, day):
        self._id = id
        self._time = time
        self._day = day

    def get_id(self): return self._id
    def get_time(self): return self._time
    def get_day(self): return self._day


class Course:
    def __init__(self, number, name, instructors, maxNumbOfStudents):
        self._number = number
        self._name = name
        self._maxNumbOfStudents = maxNumbOfStudents
        self._instructors = instructors

    def get_number(self): return self._number

    def get_name(self): return self._name

    def get_instructors(self): return self._instructors

    def get_maxNumbOfStudents(self): return self._maxNumbOfStudents

    def __str__(self): return self._name


class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses

    def get_name(self): return self._name
    def get_courses(self): return self._courses


class Section:
    def __init__(self, id, department, num_class_in_week):
        self.section_id = id
        self.department = department
        self.num_class_in_week = num_class_in_week

    def get_id(self): return self.section_id
    def get_department(self): return self.department
    def get_num_class_in_week(self): return self.num_class_in_week


class Data:

    cnx = mysql.connector.connect(
        user='root', password='', host='localhost', database='TKDB')
    conn = cnx.cursor()

    # Rooms
    conn.execute("SELECT * FROM ROOM")
    cursor = conn.fetchall()
    ROOMS = list(cursor)
    # Meeting_time
    conn.execute("SELECT * FROM M_T")
    cursor = conn.fetchall()
    MEETING_TIMES = list(cursor)
    # TEACHER
    conn.execute("SELECT * FROM TEACHER")
    cursor = conn.fetchall()
    INSTRUCTORS = list(cursor)
    # COURS
    conn.execute("SELECT * FROM COURS")
    cursor = conn.fetchall()
    COURS = list(cursor)
    # COURS Dis
    conn.execute("SELECT distinct name FROM COURS")
    cursor = conn.fetchall()
    COURS_dis = list(cursor)
    # DEPT
    conn.execute("SELECT * FROM DEPARTEMENT")
    cursor = conn.fetchall()
    DEPTS = list(cursor)
    # DEPT
    conn.execute("SELECT distinct name FROM DEPARTEMENT")
    cursor = conn.fetchall()
    DEPTS_dist = list(cursor)
    # SEC
    conn.execute("SELECT * FROM section")
    cursor = conn.fetchall()
    SECTION = list(cursor)
    # print(SECTION)
    # print(MEETING_TIMES)
    # print(INSTRUCTORS)
    # print(DEPTS_dist)
    # print(DEPTS)

    def __init__(self):
        self._rooms = []
        self._meetingTimes = []
        self._instructors = []
        self._courses = []
        self._depts = []
        self._sections = []
        for i in range(0, len(self.ROOMS)):
            self._rooms.append(Room(self.ROOMS[i][0], int(self.ROOMS[i][1])))
        for i in range(0, len(self.MEETING_TIMES)):
            self._meetingTimes.append(MeetingTime(
                self.MEETING_TIMES[i][0], self.MEETING_TIMES[i][2], self.MEETING_TIMES[i][1]))
        for i in range(0, len(self.INSTRUCTORS)):
            self._instructors.append(Instructor(
                self.INSTRUCTORS[i][0], self.INSTRUCTORS[i][1]))
        courses_depts = []
        for item in self.COURS_dis:
            teacher = []
            for i in range(0, len(self.COURS)):
                for j in range(0, len(self.INSTRUCTORS)):
                    if str(self.INSTRUCTORS[j][1]).upper() == str(self.COURS[i][3]).upper() and item[0] == str(self.COURS[i][1]).upper():
                        teacher.append(Instructor(
                            self.INSTRUCTORS[j][0], self.INSTRUCTORS[j][1]))

                if item[0] == str(self.COURS[i][1]).upper():
                    course_id = str(self.COURS[i][0])[:2]
                    course_name = self.COURS[i][1]
                    course_capacity = self.COURS[i][2]
            self._courses.append(Course(
                course_id,
                course_name,
                teacher,
                int(course_capacity)
            ))
            courses_depts.append(Course(
                course_id,
                course_name,
                teacher,
                course_capacity
            ))
        sec_depts = []
        for item in self.DEPTS_dist:
            courses = []
            for i in range(0, len(self.DEPTS)):
                for j in range(0, len(courses_depts)):
                    if str(courses_depts[j].get_name()).upper() == str(self.DEPTS[i][2]).upper() and item[0] == str(self.DEPTS[i][1]).upper():
                        courses.append(courses_depts[j])

                if item[0] == str(self.DEPTS[i][1]).upper():
                    dept_name = self.DEPTS[i][1]
            self._depts.append(Department(
                dept_name,
                courses
            ))
            sec_depts.append(Department(
                dept_name,
                courses
            ))
        for i in sec_depts:
            for j in range(0, len(self.SECTION)):
                if str(self.SECTION[j][1]).upper() == i.get_name().upper():
                    self._sections.append(Section(
                        self.SECTION[j][0],
                        i,
                        self.SECTION[j][2],
                    ))
        self._numberOfClasses = 0
        for i in range(0, len(self._depts)):
            self._numberOfClasses += len(self._depts[i].get_courses())

    def get_rooms(self): return self._rooms
    def get_instructors(self): return self._instructors
    def get_courses(self): return self._courses
    def get_depts(self): return self._depts
    def get_meetingTimes(self): return self._meetingTimes
    def get_sections(self): return self._sections
    def get_numberOfClasses(self): return self._numberOfClasses


data = Data()


class Schedule:

    def __init__(self):
        self._data = data
        self._classes = []
        self._numbOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self): return self._numbOfConflicts

    def get_fitness(self):
        if (self._isFitnessChanged == True):
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        sections = data.get_sections()
        for section in sections:
            dept = section.get_department()
            n = section.get_num_class_in_week()
            if n <= len(data.get_meetingTimes()):
                courses = dept.get_courses()
                for course in courses:
                    for i in range(n // len(courses)):
                        crs_inst = course.get_instructors()
                        newClass = Class(self._classNumb, dept,
                                         section.section_id, course)
                        self._classNumb += 1
                        newClass.set_meetingTime(data.get_meetingTimes(
                        )[rnd.randrange(0, len(data.get_meetingTimes()))])
                        newClass.set_room(
                            data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                        newClass.set_instructor(
                            crs_inst[rnd.randrange(0, len(crs_inst))])
                        self._classes.append(newClass)
            else:
                n = len(data.get_meetingTimes())
                courses = dept.get_courses()
                for course in courses:
                    for i in range(n // len(courses)):
                        crs_inst = course.get_instructors()
                        newClass = Class(self._classNumb, dept,
                                         section.section_id, course)
                        self._classNumb += 1
                        newClass.set_meetingTime(data.get_meetingTimes(
                        )[rnd.randrange(0, len(data.get_meetingTimes()))])
                        newClass.set_room(
                            data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                        newClass.set_instructor(
                            crs_inst[rnd.randrange(0, len(crs_inst))])
                        self._classes.append(newClass)
        return self

    def calculate_fitness(self):
        self._nunbOfConflicts = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):
            if (classes[i].get_room().get_seatingCapacity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._numbOfConflicts += 1
            for j in range(0, len(classes)):
                if (j >= i):
                    if (classes[i].meeting_time == classes[j].meeting_time) and \
                            (classes[i].section_id != classes[j].section_id) and (classes[i].section == classes[j].section):
                        if (classes[i].room == classes[j].room):
                            self._numbOfConflicts += 1
                        if (classes[i].instructor == classes[j].instructor):
                            self._numbOfConflicts += 1
        return 1 / ((1.0*self._numbOfConflicts + 1))

    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes)-1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str(self._classes[len(self._classes)-1])
        return returnValue


class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range(0, size):
            self._schedules.append(Schedule().initialize())

    def get_schedules(self): return self._schedules


class GeneticAlgorithm:
    def evolve(self, population): return self._mutate_population(
        self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[
                0]
            schedule2 = self._select_tournament_population(
                pop) .get_schedules()[0]
            crossover_pop.get_schedules().append(
                self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if (rnd.random() > 0.5):
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(0, len(mutateSchedule.get_classes())):
            if (MUTATION_RATE > rnd.random()):
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(
                pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class Class:
    def __init__(self, id, dept, section, course):
        self.section_id = id
        self.department = dept
        self.course = course
        self.instructor = None
        self.meeting_time = None
        self.room = None
        self.section = section

    def get_id(self): return self.section_id

    def get_dept(self): return self.department

    def get_course(self): return self.course

    def get_instructor(self): return self.instructor

    def get_meetingTime(self): return self.meeting_time

    def get_room(self): return self.room

    def set_instructor(self, instructor): self.instructor = instructor

    def set_meetingTime(self, meetingTime): self.meeting_time = meetingTime

    def set_room(self, room): self.room = room

    def __str__(self):
        return str(self.department.get_name()) + "," + str(self.course.get_number()) + "," + \
            str(self.room.get_number()) + "," + str(self.instructor.get_id()
                                                    ) + "," + str(self.meeting_time.get_id())


class DisplayMgr:
    def print_available_data(self):
        print("> All Available Data")
        self.print_dept()
        self.print_course()
        self.print_room()
        self.print_instructor()
        self.print_meeting_times()

    def print_dept(self):
        depts = data.get_depts()
        availableDeptsTable = prettytable.PrettyTable(['dept', 'courses'])
        for i in range(0, len(depts)):
            courses = depts.__getitem__(i).get_courses()
            tempStr = '['
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + ", "
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableDeptsTable.add_row(
                [depts.__getitem__(i).get_name(), tempStr])
        print(availableDeptsTable)

    def print_course(self):
        availableCoursesTable = prettytable.PrettyTable(
            ['id', 'course #', 'max # of students', 'instructors'])
        courses = data.get_courses()
        for i in range(0, len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = ""
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + ", "
            tempStr += instructors[len(instructors) - 1].__str__()
            availableCoursesTable.add_row(
                [courses[i].get_number(), courses[i].get_name(), str(courses[i].get_maxNumbOfStudents()), tempStr])
        print(availableCoursesTable)

    def print_instructor(self):
        availableInstructorsTable = prettytable.PrettyTable(
            ['id', 'instructor'])
        instructors = data.get_instructors()
        for i in range(0, len(instructors)):
            availableInstructorsTable.add_row(
                [instructors[i].get_id(), instructors[i].get_name()])
        print(availableInstructorsTable)

    def print_room(self):
        availableRoomsTable = prettytable.PrettyTable(
            ['room #', 'max seating capacity'])
        rooms = data.get_rooms()
        for i in range(0, len(rooms)):
            availableRoomsTable.add_row(
                [str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])
        print(availableRoomsTable)

    def print_meeting_times(self):
        availableMeetingTimeTable = prettytable.PrettyTable(
            ['id', 'Meeting Time'])
        meetingTimes = data.get_meetingTimes()
        for i in range(0, len(meetingTimes)):
            availableMeetingTimeTable.add_row(
                [meetingTimes[i].get_id(), meetingTimes[i].get_time()])
        print(availableMeetingTimeTable)

    def print_generation(self, population):
        table1 = prettytable.PrettyTable(
            ['schedule #', 'fitness', '# of conflicts'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            cls = ""
            for j in range(0, len(schedules[i].get_classes())-1):
                cls += schedules[i].get_classes()[j].__str__()+" ,"
            cls += schedules[i].get_classes()[len(schedules[i].get_classes()
                                                  ) - 1].__str__()
            table1.add_row([str(i), round(
                schedules[i].get_fitness(), 3), schedules[i].get_numbOfConflicts()])

        print(table1)

    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(
            ['Class #', 'section', 'Dept', 'Course(number, max # of students)', 'Room(Capacity)', 'Instructor(Id)', 'Meeting Time(Id)'])
        for i in range(0, len(classes)):
            table.add_row([str(i), classes[i].section, classes[i].get_dept().get_name(), classes[i].get_course().get_name() + "(" +
                           classes[i].get_course().get_number() + ", " +
                           str(classes[i].get_course(
                           ).get_maxNumbOfStudents()) + ")",
                           classes[i].get_room().get_number() + " (" +
                           str(classes[i].get_room(
                           ).get_seatingCapacity())+")",
                           classes[i].get_instructor().get_name() +
                           " (" +
                           str(classes[i].get_instructor().get_id())+")",
                           str(classes[i].get_meetingTime().get_day())+" ==> "+classes[i].get_meetingTime().get_time() + " (" + str(classes[i].get_meetingTime().get_id())+")"])
        print(table)


def apply():
    schedule = []
    generationNumber = 0
    population = Population(POPULATION_SIZE)
    schedule = population.get_schedules().sort(
        key=lambda x: x.get_fitness(), reverse=True)

    geneticAlgorithm = GeneticAlgorithm()
    while (population.get_schedules()[0].get_fitness() != 1.0):
        generationNumber += 1
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        schedule = population.get_schedules()[0].get_classes()
    return {
        "classes": schedule,
        "section": data.get_sections()
    }


# displayMgr = DisplayMgr()
# # displayMgr.print_available_data()
# schedule = []
# generationNumber = 0
# print("\n> Generation # "+str(generationNumber))
# population = Population(POPULATION_SIZE)
# schedule = population.get_schedules().sort(
#     key=lambda x: x.get_fitness(), reverse=True)
# displayMgr.print_generation(population)
# displayMgr.print_schedule_as_table(population.get_schedules()[0])
# geneticAlgorithm = GeneticAlgorithm()
# while (population.get_schedules()[0].get_fitness() != 1.0):
#     generationNumber += 1
#     print("\n> Generation # " + str(generationNumber))
#     population = geneticAlgorithm.evolve(population)
#     population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
#     displayMgr.print_generation(population)
#     displayMgr.print_schedule_as_table(population.get_schedules()[0])
#     schedule = population.get_schedules()[0].get_classes()
#     print("\n\n")
