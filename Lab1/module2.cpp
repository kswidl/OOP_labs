
#include <windows.h>
#include <commctrl.h>
#include <string>

namespace
{
    const char DIALOG_CLASS[] = "SliderDialogClass";

    const int ID_SLIDER = 201;
    const int ID_OK = 202;
    const int ID_CANCEL = 203;
    const int ID_VALUE = 204;

    struct SliderData
    {
        HWND slider;
        bool done;
        bool accepted;
        int value;
    };

    LRESULT CALLBACK SliderDialogProc(
        HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
    {
        SliderData* data = reinterpret_cast<SliderData*>(
            GetWindowLongPtrA(hwnd, GWLP_USERDATA));

        switch (msg)
        {
        case WM_HSCROLL:
        {
            int value = static_cast<int>(
            SendMessageA(data->slider, TBM_GETPOS, 0, 0)
            );

            SetWindowTextA(
            GetDlgItem(hwnd, ID_VALUE),
            std::to_string(value).c_str()
            );

            return 0;
        }
            
        case WM_CREATE:
        {
            CREATESTRUCTA* cs =
                reinterpret_cast<CREATESTRUCTA*>(lParam);

            data = static_cast<SliderData*>(cs->lpCreateParams);

            SetWindowLongPtrA(
                hwnd, GWLP_USERDATA,
                reinterpret_cast<LONG_PTR>(data));

            data->slider = CreateWindowExA(
                0, TRACKBAR_CLASSA, "",
                WS_CHILD | WS_VISIBLE | TBS_AUTOTICKS,
                20, 20, 340, 40,
                hwnd, (HMENU)ID_SLIDER,
                GetModuleHandleA(nullptr), nullptr);

            SendMessageA(data->slider, TBM_SETRANGE, TRUE,
                         MAKELONG(1, 100));
            SendMessageA(data->slider, TBM_SETPOS, TRUE, 1);

            CreateWindowA(
                "STATIC", "1",
                WS_CHILD | WS_VISIBLE | SS_CENTER,
                170, 55, 60, 20,
                hwnd, (HMENU)ID_VALUE,
                GetModuleHandleA(nullptr), nullptr
            );

            CreateWindowA(
                "BUTTON", "Tak",
                WS_CHILD | WS_VISIBLE | BS_DEFPUSHBUTTON,
                90, 75, 90, 30,
                hwnd, (HMENU)ID_OK,
                GetModuleHandleA(nullptr), nullptr);

            CreateWindowA(
                "BUTTON", "Vidmina",
                WS_CHILD | WS_VISIBLE,
                200, 75, 90, 30,
                hwnd, (HMENU)ID_CANCEL,
                GetModuleHandleA(nullptr), nullptr);

            return 0;
        }

        case WM_COMMAND:
            if (LOWORD(wParam) == ID_OK)
            {
                data->value = static_cast<int>(
                    SendMessageA(data->slider, TBM_GETPOS, 0, 0));

                data->accepted = true;
                data->done = true;
                DestroyWindow(hwnd);
                return 0;
            }

            if (LOWORD(wParam) == ID_CANCEL)
            {
                data->done = true;
                DestroyWindow(hwnd);
                return 0;
            }
            break;

        case WM_CLOSE:
            data->done = true;
            DestroyWindow(hwnd);
            return 0;
        }

        return DefWindowProcA(hwnd, msg, wParam, lParam);
    }
}

bool ShowSliderDialog(HWND owner, int& value)
{
    INITCOMMONCONTROLSEX controls = {};
    controls.dwSize = sizeof(controls);
    controls.dwICC = ICC_BAR_CLASSES;
    InitCommonControlsEx(&controls);

    HINSTANCE instance = GetModuleHandleA(nullptr);

    WNDCLASSA wc = {};
    wc.lpfnWndProc = SliderDialogProc;
    wc.hInstance = instance;
    wc.lpszClassName = DIALOG_CLASS;
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);

    RegisterClassA(&wc);

    SliderData data = {};
    data.done = false;
    data.accepted = false;
    data.value = 1;

    HWND dialog = CreateWindowExA(
        WS_EX_DLGMODALFRAME,
        DIALOG_CLASS,
        "Choose a number",
        WS_CAPTION | WS_SYSMENU | WS_POPUP,
        CW_USEDEFAULT, CW_USEDEFAULT,
        400, 155,
        owner, nullptr, instance, &data);

    if (dialog == nullptr)
        return false;

    EnableWindow(owner, FALSE);
    ShowWindow(dialog, SW_SHOW);
    SetForegroundWindow(dialog);

    MSG msg = {};

    while (!data.done && GetMessageA(&msg, nullptr, 0, 0) > 0)
    {
        if (!IsDialogMessageA(dialog, &msg))
        {
            TranslateMessage(&msg);
            DispatchMessageA(&msg);
        }
    }

    EnableWindow(owner, TRUE);
    SetForegroundWindow(owner);

    if (data.accepted)
    {
        value = data.value;
        return true;
    }

    return false;
}
