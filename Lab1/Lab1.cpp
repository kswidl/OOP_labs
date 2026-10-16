#include <windows.h>
#include <string>

const char CLASS_NAME[] = "Lab1Window";

#define ID_WORK1 1
#define ID_WORK2 2
#define ID_RESULT 3

bool ShowTextDialog(HWND owner, std::string& text);

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    switch (uMsg)
    {
    case WM_CREATE:
    {
        HMENU hMenu = CreateMenu();

        AppendMenuA(hMenu, MF_STRING, ID_WORK1, "Robota1");
        AppendMenuA(hMenu, MF_STRING, ID_WORK2, "Robota2");

        SetMenu(hwnd, hMenu);

        CreateWindowA(
            "STATIC", "Result will appear here",
            WS_CHILD | WS_VISIBLE,
            20, 30, 500, 30,
            hwnd, (HMENU)ID_RESULT,
            GetModuleHandleA(nullptr), nullptr
        );

        return 0;
    }

    case WM_COMMAND:
        switch (LOWORD(wParam))
        {
        case ID_WORK1:
        {
            std::string text;

            if (ShowTextDialog(hwnd, text))
            {
                SetWindowTextA(
                    GetDlgItem(hwnd, ID_RESULT),
                    text.c_str()
                );
            }

            return 0;
        }

        case ID_WORK2:
            MessageBoxA(hwnd, "Robota2 selected", "Lab1", MB_OK);
            return 0;
        }
        break;

    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }

    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, LPSTR, int nCmdShow)
{
    WNDCLASSA wc = {};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;

    RegisterClassA(&wc);

    HWND hwnd = CreateWindowExA(
        0,
        CLASS_NAME,
        "Lab1 - Windows Application",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT,
        600, 400,
        nullptr, nullptr, hInstance, nullptr
    );

    if (hwnd == nullptr)
        return 0;

    ShowWindow(hwnd, nCmdShow);

    MSG msg = {};

    while (GetMessage(&msg, nullptr, 0, 0) > 0)
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}
