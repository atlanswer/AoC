const std = @import("std");
const print = std.debug.print;

const r = @cImport(@cInclude("raylib.h"));

pub fn main() void {
    const screenWidth: c_int = 800;
    const screenHeight: c_int = 450;

    r.InitWindow(screenWidth, screenHeight, "Raylib Window Example");

    r.SetTargetFPS(144);

    while (!r.WindowShouldClose()) {
        r.BeginDrawing();

        r.ClearBackground(r.RAYWHITE);
        r.DrawText("My first Raylib window!", 190, 200, 20, r.LIGHTGRAY);

        r.EndDrawing();
    }

    r.CloseWindow();
}
