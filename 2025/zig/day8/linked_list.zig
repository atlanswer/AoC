const std = @import("std");
const print = std.debug.print;
const expect = std.testing.expect;

test "Singly Linked List" {
    var list: std.SinglyLinkedList = .{};

    const PositionNode = struct {
        node: std.SinglyLinkedList.Node = .{},
        distance: usize,
    };

    for (0..2) |i| {
        var node = PositionNode{ .distance = i };

        list.prepend(&node.node);
    }

    // try expect(list.len() == 2);
    print("first: {any}\n", .{list.first});
    print("second: {any}\n", .{list.first.?.next});
    // try expect(list.first.?.next.?.next == null);
    // const first_ptr = list.first.?;
    // const first: *PositionNode = @fieldParentPtr("node", first_ptr);
    // try expect(first.distance == 1);
    // const second_ptr = list.first.?.next.?;
    // const second: *PositionNode = @fieldParentPtr("node", second_ptr);
    // try expect(second.distance == 0);
}

test "example" {
    var list: std.SinglyLinkedList = .{};

    const L = struct {
        data: usize,
        node: std.SinglyLinkedList.Node = .{},
    };

    try expect(list.len() == 0);

    // var zero = L{.data = 0};
    var one = L{ .data = 1 };
    var two = L{ .data = 2 };

    list.prepend(&two.node);
    try expect(list.first.?.next == null);
    list.prepend(&one.node);
    try expect(list.first.?.next.?.next == null);

    list = .{};

    try expect(list.len() == 0);

    for (0..2) |i| {
        var node = L{ .data = i };

        print("\nnew node: {any}, addr: {*}\n", .{ node, &node });

        print("\nbefore prepend:\n", .{});
        if (list.first == null) {
            print("list is empty\n", .{});
        } else {
            const first_ptr: *L = @fieldParentPtr("node", list.first.?);
            print("first item: {any}, addr: {*}\n", .{ first_ptr, first_ptr });
        }

        list.prepend(&node.node);

        print("after prepend:\n", .{});
        if (list.first == null) {
            print("list is empty\n\n", .{});
        } else {
            const first_ptr: *L = @fieldParentPtr("node", list.first.?);
            print("first item: {any}, addr: {*}\n", .{ first_ptr, first_ptr });
        }
    }
    try expect(list.first.?.next.?.next == null);
}
