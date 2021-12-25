#!/usr/bin/env python
import math
from collections import namedtuple
from enum import Enum, IntEnum

Packet = namedtuple("Packet", "version type_id value subpackets")

def hex2bin(s):
    return "".join("{:04b}".format(int(c, 16)) for c in s)


class State(Enum):
    Header = "header"
    Literal = "literal"
    Operator = "operator"


class Type(IntEnum):
    Sum = 0
    Product = 1
    Minimum = 2
    Maximum = 3
    Literal = 4
    GreaterThan = 5
    LessThan = 6
    EqualTo = 7


class Stream:
    def __init__(self, s):
        self.bits = hex2bin(s)
        self.pos = 0

    def read(self, n):
        new_pos = self.pos + n
        assert new_pos <= len(self.bits)
        chunk = self.bits[self.pos:new_pos]
        self.pos = new_pos
        return chunk

    @property
    def remaining(self):
        return len(self.bits) - self.pos


def parse_packet(stream, outer=True):
    version, type_id, value = None, None, None
    subpackets, subpackets_len, subpackets_num = None, None, None
    state = State.Header

    while stream.remaining:
        if state is State.Header:
            version = int(stream.read(3), 2)
            type_id = int(stream.read(3), 2)
        elif state is State.Literal:
            chunks = []
            while stream.read(1) == "1":
                chunks.append(stream.read(4))
            chunks.append(stream.read(4))
            value = int("".join(chunks), 2)
        elif state is State.Operator:
            subpackets = []
            length_type_id = stream.read(1)
            if length_type_id == "0":
                subpackets_len = int(stream.read(15), 2)
                read_until = stream.pos + subpackets_len
                while stream.pos < read_until:
                    packet = parse_packet(stream, outer=False)
                    subpackets.append(packet)
            elif length_type_id == "1":
                subpackets_num = int(stream.read(11), 2)
                packets_read = 0
                while packets_read < subpackets_num:
                    packet = parse_packet(stream, outer=False)
                    subpackets.append(packet)
                    packets_read += 1

        if state is State.Header:
            if type_id == Type.Literal:
                state = State.Literal
            else:
                state = State.Operator
        else:
            if outer:
                padding_len = -stream.pos % 4
                padding = stream.read(padding_len)
                assert padding == "0" * padding_len
            return Packet(version=version, type_id=type_id, value=value, subpackets=subpackets)

    raise RuntimeError("Failed to parse packet")


def iter_version_numbers(packet):
    yield packet.version
    for subpacket in packet.subpackets or []:
        yield from iter_version_numbers(subpacket)


def evaluate(packet):
    if packet.type_id == Type.Sum:
        return sum(evaluate(p) for p in packet.subpackets)
    elif packet.type_id == Type.Product:
        return math.prod(evaluate(p) for p in packet.subpackets)
    elif packet.type_id == Type.Minimum:
        return min(evaluate(p) for p in packet.subpackets)
    elif packet.type_id == Type.Maximum:
        return max(evaluate(p) for p in packet.subpackets)
    elif packet.type_id == Type.Literal:
        return packet.value
    elif packet.type_id == Type.GreaterThan:
        a, b = packet.subpackets
        return 1 if evaluate(a) > evaluate(b) else 0
    elif packet.type_id == Type.LessThan:
        a, b = packet.subpackets
        return 1 if evaluate(a) < evaluate(b) else 0
    elif packet.type_id == Type.EqualTo:
        a, b = packet.subpackets
        return 1 if evaluate(a) == evaluate(b) else 0

    raise RuntimeError(f"Invalid packet type: {packet.type_id}")


def main():
    assert hex2bin("D2FE28") == "110100101111111000101000"
    assert parse_packet(Stream("D2FE28")) == Packet(
        version=6,
        type_id=4,
        value=2021,
        subpackets=None,
    )
    assert parse_packet(Stream("38006F45291200")) == (
        Packet(
            version=1,
            type_id=6,
            value=None,
            subpackets=[
                Packet(version=6, type_id=4, value=10, subpackets=None),
                Packet(version=2, type_id=4, value=20, subpackets=None),
            ],
        )
    )
    assert parse_packet(Stream("EE00D40C823060")) == (
        Packet(
            version=7,
            type_id=3,
            value=None,
            subpackets=[
                Packet(version=2, type_id=4, value=1, subpackets=None),
                Packet(version=4, type_id=4, value=2, subpackets=None),
                Packet(version=1, type_id=4, value=3, subpackets=None),
            ],
        )
    )

    assert evaluate(parse_packet(Stream("C200B40A82"))) == 3

    with open("input.txt") as f:
        transmission = f.read().strip()
        packet = parse_packet(Stream(transmission))

    print("part 1")
    print(sum(iter_version_numbers(packet)))

    print("part 2")
    print(evaluate(packet))


if __name__ == "__main__":
    main()
