# RWR_Borderless_Fullscreen_Extension

This extension can auto detect game process and set RUNNING WITH RIFLES game window to borderless fullscreen mode. In borderless fullscreen mode, the game can be switched directly to other desktop windows without going through black screen or screen flickering. This is very helpful for game development or chatting with other player while playing game.

# Demo
<div align=center><img src="./assets/demo.webp"/></div>

# Adding to the game

If you are the game developer, you can add these lines to game window (hwnd) initializing code to achieve the same feature:

```cpp
// need to add a new borderless fullscreen config value to rwr_config.exe
if (get_game_config_fullscreen_mode() == BORDERLESS_FULLSCREEN)
{
    LONG game_window_style = GetWindowLong(g_hwnd, GWL_STYLE);
    game_window_style &= ~(WS_BORDER | WS_DLGFRAME | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX);
    SetWindowLong(g_hwnd, GWL_STYLE, game_window_style);
}
```

# Known Issues

Borderless fullscreen mode will forece the game running on the same resolution of system. This is a problem (or feature) of borderless fullscreen mode itself, and is unsolvable unless you can stretch the output graphics. But I think there is no need to solve it because RWR doesn't require much PC performance, most players can run this game on their screen resolution.