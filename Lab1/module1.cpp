
#include <windows.h>
#include <string>

namespace
{
    const char DIALOG_CLASS[] = "TextDialogClass";

    const int ID_EDIT = 101;
    const int ID_OK = 102;
    const int ID_CANCEL = 103;

    struct DialogData
    {
        HWND edit;
        bool done;
        bool accepted;
        std::string text;
    };

    LRESULT CALLBACK TextDialogProc(
        HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
    {
        DialogData* data = reinterpret_cast<DialogData*>(
            GetWindowLongPtrA(hwnd, GWLP_USERDATA));

        switch (msg)
        {
        case WM_CREATE:
        {
            CREATESTRUCTA* cs =
                reinterpret_cast<CREATESTRUCTA*>(lParam);

            data = static_cast<DialogData*>(cs->lpCreateParams);

            SetWindowLongPtrA(
                hwnd, GWLP_USERDATA,
                reinterpret_cast<LONG_PTR>(data));

            data->edit = CreateWindowExA(
                WS_EX_CLIENTEDGE, "EDIT", "",
                WS_CHILD | WS_VISIBLE | ES_AUTOHSCROLL,
                20, 20, 340, 28,
                hwnd, (HMENU)ID_EDIT,
                GetModuleHandleA(nullptr), nullptr);

            CreateWindowA(
                "BUTTON", "Tak",
                WS_CHILD | WS_VISIBLE | BS_DEFPUSHBUTTON,
                90, 65, 90, 30,
                hwnd, (HMENU)ID_OK,
                GetModuleHandleA(nullptr), nullptr);

            CreateWindowA(
                "BUTTON", "Vidmina",
                WS_CHILD | WS_VISIBLE,
                200, 65, 90, 30,
                hwnd, (HMENU)ID_CANCEL,
                GetModuleHandleA(nullptr), nullptr);

            return 0;
        }

        case WM_COMMAND:
            if (LOWORD(wParam) == ID_OK)
            {
                int length = GetWindowTextLengthA(data->edit);
                std::string value(length + 1, '\0');

                GetWindowTextA(
                    data->edit, &value[0], length + 1);

                value.resize(length);
                data->text = value;
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

bool ShowTextDialog(HWND owner, std::string& text)
{
    HINSTANCE instance = GetModuleHandleA(nullptr);

    WNDCLASSA wc = {};
    wc.lpfnWndProc = TextDialogProc;
    wc.hInstance = instance;
    wc.lpszClassName = DIALOG_CLASS;
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);

    RegisterClassA(&wc);

    DialogData data = {};
    data.done = false;
    data.accepted = false;

    HWND dialog = CreateWindowExA(
        WS_EX_DLGMODALFRAME,
        DIALOG_CLASS,
        "Vvedit tekst",
        WS_CAPTION | WS_SYSMENU | WS_POPUP,
        CW_USEDEFAULT, CW_USEDEFAULT,
        400, 145,
        owner, nullptr, instance, &data);

    if (dialog == nullptr)
        return false;

    EnableWindow(owner, FALSE);
    ShowWindow(dialog, SW_SHOW);
    SetForegroundWindow(dialog);
    SetFocus(data.edit);

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
        text = data.text;
        return true;
    }

    return false;
}
