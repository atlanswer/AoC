const std = @import("std");
const assert = std.debug.assert;

pub fn getInput(allocator: std.mem.Allocator) ![]u8 {
    var threaded: std.Io.Threaded = .init_single_threaded;
    defer threaded.deinit();

    const io: std.Io = threaded.io();

    const cwd = try std.process.getCwdAlloc(allocator);
    const AOC_DAY = std.fs.path.basename(cwd);
    const input_file_path = try std.fs.path.resolve(allocator, &.{ cwd, "..", "..", "input", AOC_DAY, "input.txt" });

    const input_file = std.Io.Dir.openFileAbsolute(io, input_file_path, .{}) catch |err|
        switch (err) {
            std.Io.File.OpenError.FileNotFound => {
                std.debug.print("[ERROR] File `{s}` not found.\n", .{input_file_path});
                std.process.exit(1);
            },
            else => return err,
        };
    defer input_file.close(io);

    const buffer: []u8 = try allocator.alloc(u8, try input_file.length(io));

    const read_len = try input_file.readPositionalAll(io, buffer, 0);
    assert(read_len == buffer.len);

    return buffer;
}

pub fn timeIt(comptime func: fn () anyerror!void) !void {
    var timer = try std.time.Timer.start();
    try func();
    std.debug.print(
        "Execution time: {d} ms.\n",
        .{@as(f64, @floatFromInt(timer.lap())) / std.time.ns_per_ms},
    );
}
