#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::error::Error;

use slint::LogicalPosition;

slint::include_modules!();

fn main() -> Result<(), Box<dyn Error>> {
    let ui = AppWindow::new()?;

    let ui_weak = ui.as_weak();
    let ui_weak_minimize = ui.as_weak();

    ui.on_move_window(move |x, y| {
        if let Some(ui) = ui_weak.upgrade() {
            let window = ui.window();
            let logical_pos = window.position().to_logical(window.scale_factor());
            window.set_position(LogicalPosition::new(
                logical_pos.x + x,
                logical_pos.y + y,
            ));
        }
    });

    ui.on_minimize_window(move || {
        if let Some(ui) = ui_weak_minimize.upgrade() {
            ui.window().set_minimized(true);
        }
    });

    ui.on_close_window(|| {
        std::process::exit(0);
    });

    ui.run()?;

    Ok(())
}
