const std = @import("std");

pub fn getInput(allocator: std.mem.Allocator) ![]u8 {
    const cwd = try std.process.getCwdAlloc(allocator);
    const AOC_DAY = std.fs.path.basename(cwd);
    const input_file_path = try std.fs.path.resolve(allocator, &.{ cwd, "..", "..", "input", AOC_DAY, "input.txt" });

    const input_file = std.fs.openFileAbsolute(input_file_path, .{}) catch |err| {
        if (err == std.Io.File.OpenError.FileNotFound) {
            std.debug.print("[ERROR] File `{s}` not found.\n", .{input_file_path});
            std.process.exit(1);
        }
        return err;
    };
    defer input_file.close();

    var threaded = std.Io.Threaded.init(allocator);
    defer threaded.deinit();

    var reader = input_file.reader(threaded.io(), try allocator.alloc(u8, 1024));

    return try reader.interface.allocRemaining(allocator, .unlimited);
}

pub fn timeIt(comptime func: fn () anyerror!void) !void {
    var timer = try std.time.Timer.start();
    try func();
    std.debug.print(
        "Execution time: {d} ms.\n",
        .{@as(f64, @floatFromInt(timer.lap())) / std.time.ns_per_ms},
    );
}
