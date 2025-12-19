const std = @import("std");
const print = std.debug.print;
const assert = std.debug.assert;
const expect = std.testing.expect;
const getInput = @import("aoc-utils.zig").getInput;
const timeIt = @import("aoc-utils.zig").timeIt;

test "Execution time" {
    try timeIt(main);
}

var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
const allocator = arena.allocator();

pub fn main() !void {
    defer arena.deinit();

    const input =
        \\[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        \\[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        \\[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
    ;
    // const input = try getInput(allocator);

    var res: usize = 0;

    var input_it = std.mem.splitScalar(u8, std.mem.trim(u8, input, "\n"), '\n');
    while (input_it.next()) |line| : ({}) {
        // print("{s}\n", .{line});

        var buttons: std.ArrayList(@Vector(8, usize)) = .empty;
        var joltages: @Vector(8, usize) = undefined;

        var section_it = std.mem.splitScalar(u8, line, ' ');
        while (section_it.next()) |section| {
            // Light diagram
            // if (section[0] == '[' and section[section.len - 1] == ']') {}
            // Button wiring schematic
            if (section[0] == '(' and section[section.len - 1] == ')') {
                var wire_it = std.mem.splitScalar(u8, section[1 .. section.len - 1], ',');
                var button_arr: [8]usize = .{ 0, 0, 0, 0, 0, 0, 0, 0 };
                while (wire_it.next()) |wire_s| {
                    const wire: usize = try std.fmt.parseInt(usize, wire_s, 10);
                    button_arr[wire] = 1;
                }
                const button: @Vector(8, usize) = button_arr;
                try buttons.append(allocator, button);
            }
            // Joltage requirement
            if (section[0] == '{' and section[section.len - 1] == '}') {
                var joltage_it = std.mem.splitScalar(u8, section[1 .. section.len - 1], ',');
                var idx: usize = 0;
                var joltage_arr: [8]usize = .{ 0, 0, 0, 0, 0, 0, 0, 0 };
                while (joltage_it.next()) |joltage_s| : (idx += 1) {
                    const joltage = try std.fmt.parseInt(usize, joltage_s, 10);
                    joltage_arr[idx] = joltage;
                }
                joltages = joltage_arr;
            }
        }
        // print("lights: {b:0>16}\n", .{lights});

        std.mem.sortUnstable(@Vector(8, usize), buttons.items, {}, struct {
            fn greaterThanFn(_: void, a: @Vector(8, usize), b: @Vector(8, usize)) bool {
                const sa: usize = @reduce(.Add, a);
                const sb: usize = @reduce(.Add, b);
                return sa > sb;
            }
        }.greaterThanFn);

        print("button:\n", .{});
        for (buttons.items) |button| {
            print("{any}\n", .{button});
        }
        print("joltages: {}\n", .{joltages});

        var step: usize = 0;

        var cur_joltages: @Vector(8, usize) = .{ 0, 0, 0, 0, 0, 0, 0, 0 };
        var idx: usize = 0;

        while (true) {
            if (@reduce(.And, cur_joltages == joltages)) break;

            assert(idx < buttons.items.len);
            print("idx: {}\n", .{idx});

            while (true) {
                const next_joltages = cur_joltages + buttons.items[idx];
                if (@reduce(.Or, next_joltages > joltages)) break;
                print("using: {}\n", .{buttons.items[idx]});
                cur_joltages = next_joltages;
                print("after: {}\n", .{cur_joltages});
                step += 1;
            }

            idx += 1;
        }

        print("step: {}\n", .{step});
        res += step;
    }

    print("res: {}\n", .{res});
}
