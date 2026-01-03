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

const counter_len = 16;
const Counter = @Vector(counter_len, usize);

pub fn main() !void {
    defer arena.deinit();

    // const input =
    //     \\[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    //     \\[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
    //     \\[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
    // ;
    const input = try getInput(allocator);

    var res: usize = 0;

    var input_it = std.mem.splitScalar(u8, std.mem.trim(u8, input, "\n"), '\n');
    while (input_it.next()) |line| : ({}) {
        // print("{s}\n", .{line});

        var buttons: std.ArrayList(Counter) = .empty;
        var joltages: Counter = undefined;

        var section_it = std.mem.splitScalar(u8, line, ' ');
        while (section_it.next()) |section| {
            // Light diagram
            // if (section[0] == '[' and section[section.len - 1] == ']') {}

            // Button wiring schematic
            if (section[0] == '(' and section[section.len - 1] == ')') {
                var button_arr: [counter_len]usize = undefined;
                @memset(&button_arr, 0);
                var wire_it = std.mem.splitScalar(u8, section[1 .. section.len - 1], ',');
                while (wire_it.next()) |wire_s| {
                    const wire: usize = try std.fmt.parseInt(usize, wire_s, 10);
                    button_arr[wire] = 1;
                }
                const button: Counter = button_arr;
                try buttons.append(allocator, button);
            }

            // Joltage counter
            if (section[0] == '{' and section[section.len - 1] == '}') {
                var idx: usize = 0;
                var joltage_arr: [counter_len]usize = undefined;
                @memset(&joltage_arr, 0);
                var joltage_it = std.mem.splitScalar(u8, section[1 .. section.len - 1], ',');
                while (joltage_it.next()) |joltage_s| : (idx += 1) {
                    const joltage = try std.fmt.parseInt(usize, joltage_s, 10);
                    joltage_arr[idx] = joltage;
                }
                joltages = joltage_arr;
            }
        }

        // print("button:\n", .{});
        // for (buttons.items) |button| {
        //     print("{any}\n", .{button});
        // }
        // print("joltages: {}\n", .{joltages});

        const step: usize = try findPresses(joltages, buttons);
        print("------------------------step: {d}\n", .{step});

        // res += 1;
        res += step;
    }

    print("res: {}\n", .{res});
}

fn findPresses(joltages: Counter, buttons: std.ArrayList(Counter)) (error{Unsolvable} || std.mem.Allocator.Error)!usize {
    // print("current joltages: {}\n", .{joltages});
    assert(@reduce(.Add, joltages) != 0);

    // Not all even
    if (@reduce(
        .And,
        joltages % @as(Counter, @splat(2)) == @as(Counter, @splat(0)),
    )) {
        return try findPresses(joltages / @as(Counter, @splat(2)), buttons) * 2;
    }

    const max_joltage: usize = @reduce(.Max, joltages);
    assert(max_joltage != 0);

    var candidate_presses: std.ArrayList(usize) = .empty;
    var matching_presses: std.ArrayList(usize) = .empty;

    for (1..max_joltage + 1) |cur_max_joltage| {
        if (cur_max_joltage > buttons.items.len) break;

        const comb = try combination(buttons.items.len, cur_max_joltage);

        for (comb.items) |presses| {
            var res_joltages: Counter = @splat(0);
            for (presses.items) |b| {
                res_joltages += buttons.items[b];
            }
            // match
            if (@reduce(.And, res_joltages == joltages)) {
                // print("matched!, with {any}\n", .{presses});
                try matching_presses.append(allocator, presses.items.len);
                continue;
            }
            // same parity
            if (@reduce(
                .And,
                res_joltages % @as(Counter, @splat(2)) ==
                    joltages % @as(Counter, @splat(2)),
            )) {
                // no overcount
                if (@reduce(.And, res_joltages <= joltages)) {
                    const remaining_presses = findPresses(
                        (joltages - res_joltages) / @as(Counter, @splat(2)),
                        buttons,
                    ) catch |err| switch (err) {
                        error.Unsolvable => continue,
                        else => return err,
                    };
                    // print("presses: {any}, len: {}\n", .{ presses, presses.items.len });
                    // print("res_joltages: {any}\n", .{res_joltages});
                    // print("presses + candidate: {} + {} * 2\n", .{ presses.items.len, remaining_presses });
                    try candidate_presses.append(
                        allocator,
                        presses.items.len + remaining_presses * 2,
                    );
                }
            }
        }
    }

    const min_matching: ?usize = if (matching_presses.items.len > 0)
        std.mem.min(usize, matching_presses.items)
    else
        null;
    const min_candidate: ?usize = if (candidate_presses.items.len > 0)
        std.mem.min(usize, candidate_presses.items)
    else
        null;

    // print("button:\n", .{});
    // for (buttons.items) |button| {
    //     print("{any}\n", .{button});
    // }
    // print("joltages: {}\n", .{joltages});

    if (min_matching == null and min_candidate == null) return error.Unsolvable;
    if (min_matching == null) return min_candidate.?;
    if (min_candidate == null) return min_matching.?;
    return if (min_candidate.? < min_matching.?) min_candidate.? else min_matching.?;
}

fn combination(n: usize, k: usize) std.mem.Allocator.Error!std.ArrayList(std.ArrayList(usize)) {
    assert(k >= 1);
    assert(n >= k);

    var result: std.ArrayList(std.ArrayList(usize)) = .empty;
    var idxs: std.ArrayList(usize) = try .initCapacity(allocator, k);
    for (0..k) |idx| idxs.appendAssumeCapacity(idx);

    outer: while (true) {
        try result.append(allocator, try idxs.clone(allocator));

        var i: usize = k - 1;
        while (idxs.items[i] == n - k + i) : ({
            if (i == 0) break :outer;
            i -= 1;
        }) {}

        idxs.items[i] += 1;
        for (i + 1..k) |nidx| idxs.items[nidx] = idxs.items[nidx - 1] + 1;
    }

    return result;
}
