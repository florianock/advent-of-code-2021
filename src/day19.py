#!/usr/bin/env python3
import copy
import re
from dataclasses import dataclass
from math import sqrt

from aocd import data, submit

# --- Day 19: Beacon scanner ---


def main():
    b1 = solve(basic, 3)
    assert b1 == 3, f"expected 3, but got {b1}"
    ex1 = solve(example)
    assert ex1 == 79, f"expected 79, but got {ex1}"
    # print(data)


def solve(inputs: str, match_criteria: int = 12) -> int:
    reports = inputs.split('\n\n')
    # 1. Create scanners
    scanners = [Scanner(r) for r in reports]
    # 2. We use scanner 0 as reference
    scanner = next(s for s in scanners if s.id == 0)
    scanner.position = Point(0, 0, 0)
    beacons = set(scanner.get_beacons())
    for s in scanners:
        if s is scanner or s in scanner.network:
            continue
        overlap = scanner.find_overlap(s, match_criteria)
        if overlap:
            match = overlap.popitem()
            scanner_beacon, other_beacon = match[0], match[1]
            new_x = scanner_beacon.position.x - other_beacon.position.x
            new_y = scanner_beacon.position.y - other_beacon.position.y
            new_z = scanner_beacon.position.z - other_beacon.position.z
            s.set_position(Point(new_x, new_y, new_z))
            beacons.update(s.get_beacons())
            scanner.network.add(s)
    return len(beacons)


@dataclass
class Point:
    """
    Basic 3D Point class that has a method to calculate the Pythagorean distance to some given point and a method
    to readjust it's position according to some new origin
    """
    x: int
    y: int
    z: int

    def distance(self, point) -> int:
        pythagoras = abs(self.x - point.x) ** 2 + abs(self.y - point.y) ** 2 + abs(self.z - point.z) ** 2
        return int(sqrt(pythagoras))

    def set_origin(self, point):
        self.x = point.x + self.x
        self.y = point.y + self.y
        self.z = point.z + self.z

    def rotate(self):
        yield Point(self.x, self.z, self.y)
        yield Point(self.y, self.x, self.z)
        yield Point(self.x, self.y, self.z)
        yield Point(self.y, self.z, self.x)
        yield Point(self.z, self.x, self.y)
        yield Point(self.z, self.y, self.x)
        for p in self.orientations():
            yield p
        # for p in self.orientations(Point(self.x, self.y, self.z)):
        #     yield p
        # for p in self.orientations(Point(self.x, self.z, self.y)):
        #     yield p
        # for p in self.orientations(Point(self.y, self.x, self.z)):
        #     yield p
        #
        # for p in self.orientations(Point(self.y, self.z, point.x)):
        #     yield self
        # for p in self.orientations(Point(self.z, point.x, point.y)):
        #     yield p
        # for p in self.orientations(Point(self.z, point.y, point.x)):
        #     yield p

    def orientations(self):
        yield Point(self.x * -1, self.y, self.z)
        yield Point(self.x, self.y * -1, self.z)
        yield Point(self.x, self.y, self.z * -1)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __lt__(self, other):
        return self.__hash__() < other.__hash__()

    def __hash__(self):
        return hash(self.__key__())

    def __key__(self) -> tuple:
        return self.x, self.y, self.z


@dataclass
class Beacon:
    """
    A Beacon knows all distances to other beacons
    """
    position: Point
    distances: []

    def set_distances(self, beacons: list[Point]):
        for b in beacons:
            dist = self.position.distance(b)
            self.distances.append(dist)
            self.distances.sort()

    def find_common(self, beacon) -> list[int]:
        return [i for i in beacon.distances if i in self.distances]

    def normalize_position(self, origin: Point):
        self.position.set_origin(origin)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __lt__(self, other):
        return self.__hash__() < other.__hash__()

    def __hash__(self):
        return hash(self.__key__())

    def __key__(self) -> tuple:
        return self.position.__key__()


class Scanner:
    """
    A scanner knows beacons.
    """
    def __init__(self, report: str):
        self.beacons: list[Beacon] = []
        self.position: Point = None
        self.network: set[Scanner] = {self}
        lines = report.split('\n')
        n = re.findall(r'(\d+)', lines[0])
        self.id = int(n[0])
        for line in lines[1:]:
            self.add_beacon(line)
        beacon_positions = [b.position for b in self.beacons]
        for b in self.beacons:
            b.set_distances(beacon_positions)

    def add_beacon(self, coordinates: str):
        nums = coordinates.split(',')
        x, y = nums[0], nums[1]
        if len(nums) == 2:
            z = '0'
        else:
            z = nums[2]
        pos = Point(int(x), int(y), int(z))
        self.beacons.append(Beacon(pos, []))

    def find_overlap(self, scanner, threshold: int) -> dict:
        result = {}
        for s in self.network:
            for b in s.get_beacons():
                match = None
                for c in scanner.get_beacons():
                    common_distances = b.find_common(c)
                    if len(common_distances) >= threshold:
                        match = c
                        break
                if match:
                    result[b] = match
        return result

    def set_position(self, pos: Point):
        self.position = pos
        for b in self.beacons:
            b.normalize_position(self.position)

    def get_beacons(self) -> list[Beacon]:
        return copy.deepcopy(self.beacons)


basic = """
--- scanner 0 ---
0,2
4,1
3,3

--- scanner 1 ---
-1,-1
-5,0
-2,1
""".strip()


example = """
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
""".strip()

if __name__ == "__main__":
    main()
