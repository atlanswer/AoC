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

    // const input =
    //     \\[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    //     \\[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
    //     \\[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
    // ;
    const input = try getInput(allocator);

    var min_light: usize = std.math.maxInt(usize);
    var max_light: usize = 0;
    var min_button: usize = std.math.maxInt(usize);
    var max_button: usize = 0;

    var input_it = std.mem.splitScalar(u8, std.mem.trim(u8, input, "\n"), '\n');
    while (input_it.next()) |line| : ({}) {
        // print("{s}\n", .{line});
        var buttons = std.ArrayList([]const u8).empty;

        var section_it = std.mem.splitScalar(u8, line, ' ');
        while (section_it.next()) |section| {
            // Light diagram
            if (section[0] == '[' and section[section.len - 1] == ']') {
                const l = section.len - 2;
                if (l > max_light) max_light = l;
                if (l < min_light) min_light = l;
            }
            // Button wiring schematic
            if (section[0] == '(' and section[section.len - 1] == ')') {
                try buttons.append(allocator, section[1 .. section.len - 1]);
            }
            // Joltage requirement
            // if (section[0] == '{' and section[section.len - 1] == '}') {}

        }

        if (buttons.items.len > max_button) max_button = buttons.items.len;
        if (buttons.items.len < min_button) min_button = buttons.items.len;
    }

    print("min light: {}\n", .{min_light});
    print("max light: {}\n", .{max_light});
    print("min button: {}\n", .{min_button});
    print("max button: {}\n", .{max_button});
}

fn switchLight(light: u16, button: u16) u16 {
    return (~light & button) | (light & ~button);
}

fn combination(n: usize, k: usize) !std.ArrayList(std.ArrayList(usize)) {
    var result: std.ArrayList(std.ArrayList(usize)) = .empty;
    var idxs: std.ArrayList(usize) = try .initCapacity(allocator, k);

    while (true) {}

    return result;
}
