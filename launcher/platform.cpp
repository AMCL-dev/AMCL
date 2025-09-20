#include "platform.h"
#include <map>
#include <string>
#include <locale>
#include <codecvt>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <memory>

#ifdef _WIN32
    #include <windows.h>
    #include <shlobj.h>
    #include "WinToast/include/wintoastlib.h"
    using namespace WinToastLib;
#elif __APPLE__
    #include <TargetConditionals.h>
    #include <CoreFoundation/CoreFoundation.h>
#else
    #include <unistd.h>
    #include <libnotify/notify.h>
#endif

std::map<std::string, std::map<std::string, std::string>> i18n_messages = {
    {"toast_title", {
        {"zh-CN", "AMCL正在准备中"},
        {"zh-TW", "AMCL正在準備中"},
        {"en", "AMCL is preparing"},
        {"de", "AMCL wird vorbereitet"},
        {"ja", "AMCLの準備中"},
        {"fr", "AMCL en préparation"},
        {"it", "AMCL in preparazione"},
        {"ar", "AMCL يجري التحضير"},
        {"ru", "AMCL готовится"}
    }},
    {"toast_message", {
        {"zh-CN", "初次启动耗时可能较长，请耐心等待"},
        {"zh-TW", "初次啟動耗時可能較長，請耐心等待"},
        {"en", "Initial startup may take longer, please wait patiently"},
        {"de", "Der erste Start kann länger dauern, bitte haben Sie Geduld"},
        {"ja", "初回起動には時間がかかる場合がありますので、しばらくお待ちください"},
        {"fr", "Le premier démarrage peut prendre plus de temps, veuillez patienter"},
        {"it", "L'avvio iniziale potrebbe richiedere più tempo, si prega di attendere"},
        {"ar", "قد تستغرق عملية البدء الأولى وقتًا أطول، يرجى التحلي بالصبر"},
        {"ru", "Первоначальный запуск может занять больше времени, пожалуйста, подождите"}
    }},
    {"error_title", {
        {"zh-CN", "错误"},
        {"zh-TW", "錯誤"},
        {"en", "Error"},
        {"de", "Fehler"},
        {"ja", "エラー"},
        {"fr", "Erreur"},
        {"it", "Errore"},
        {"ar", "خطأ"},
        {"ru", "Ошибка"}
    }},
    {"error_message", {
        {"zh-CN", "AMCL启动器遇到无法解决的严重问题，异常退出。已将启动器日志保存到 %s，请凭此日志联系开发者寻求解决方案"},
        {"zh-TW", "AMCL啟動器遇到無法解決的嚴重問題，異常退出。已將啟動器日誌保存到 %s，請憑此日誌聯繫開發者尋求解決方案"},
        {"en", "AMCL launcher encountered a critical issue and exited abnormally. Logs saved to %s. Please provide this log to the developer for assistance"},
        {"de", "AMCL-Launcher ist auf ein kritisches Problem gestoßen und wurde unerwartet beendet. Protokolle gespeichert unter %s. Bitte geben Sie dieses Protokoll an den Entwickler weiter"},
        {"ja", "AMCLランチャーが重大な問題に遭遇し異常終了しました。ログは %s に保存されました。開発者にこのログを提供してください"},
        {"fr", "Le lanceur AMCL a rencontré un problème critique et s'est arrêté anormalement. Les journaux sont enregistrés dans %s. Veuillez fournir ce journal au développeur"},
        {"it", "Il launcher AMCL ha riscontrato un problema critico ed è uscito in modo anomalo. Log salvati in %s. Fornire questo log allo sviluppatore"},
        {"ar", "واجه مشغل AMCL مشكلة حرجة وخرج بشكل غير طبيعي. تم حفظ السجلات في %s. يرجى تقديم هذا السجل إلى المطور"},
        {"ru", "Запускатор AMCL столкнулся с критической проблемой и завершил работу аварийно. Логи сохранены в %s. Предоставьте этот журнал разработчику"}
    }}
};

// 获取系统语言
std::string get_system_language() {
    #ifdef _WIN32
        wchar_t localeName[LOCALE_NAME_MAX_LENGTH] = {0};
        if (GetUserDefaultLocaleName(localeName, LOCALE_NAME_MAX_LENGTH) > 0) {
            std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
            return converter.to_bytes(localeName);
        }
    #elif __APPLE__
        CFLocaleRef locale = CFLocaleCopyCurrent();
        CFStringRef lang = CFLocaleGetIdentifier(locale);
        CFIndex length = CFStringGetLength(lang) + 1;
        char* buffer = new char[length];
        if (CFStringGetCString(lang, buffer, length, kCFStringEncodingUTF8)) {
            std::string result(buffer);
            delete[] buffer;
            CFRelease(locale);
            return result;
        }
        delete[] buffer;
        CFRelease(locale);
    #else
        const char* lang = std::getenv("LANG");
        if (lang) {
            std::string result(lang);
            size_t underscore_pos = result.find('_');
            if (underscore_pos != std::string::npos) {
                result[underscore_pos] = '-';
            }
            size_t dot_pos = result.find('.');
            if (dot_pos != std::string::npos) {
                result = result.substr(0, dot_pos);
            }
            return result;
        }
    #endif
    return "en";
}

std::wstring i18n(const std::string &key)
{
    std::string lang = get_system_language();

    auto key_iter = i18n_messages.find(key);
    if (key_iter == i18n_messages.end()) {
        return L"";
    }

    auto lang_iter = key_iter->second.find(lang);
    if (lang_iter != key_iter->second.end()) {
        std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
        return converter.from_bytes(lang_iter->second);
    }

    std::string primary_lang = lang.substr(0, 2);
    for (const auto& entry : key_iter->second) {
        if (entry.first.substr(0, 2) == primary_lang) {
            std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
            return converter.from_bytes(entry.second);
        }
    }

    lang_iter = key_iter->second.find("en");
    if (lang_iter != key_iter->second.end()) {
        std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
        return converter.from_bytes(lang_iter->second);
    }

    if (!key_iter->second.empty()) {
        std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
        return converter.from_bytes(key_iter->second.begin()->second);
    }

    return L"";
}

#ifdef _WIN32
class MWinToastHandler : public IWinToastHandler
{
public:
    void toastActivated() const override { std::wcout << L"Active!"; }
    void toastActivated(int actionIndex) const override { std::wcout << L"Active!"; }
    void toastActivated(std::wstring respons) const override { std::wcout << L"Active!"; }
    void toastDismissed(WinToastDismissalReason state) const override { std::wcout << L"Dismissed!"; }
    void toastFailed() const override { std::wcout << L"Failed!"; }
};

// 获取当前可执行文件路径
std::wstring get_executable_path() {
    wchar_t path[MAX_PATH];
    GetModuleFileNameW(NULL, path, MAX_PATH);
    return std::wstring(path);
}

// 获取图标路径
std::wstring get_icon_path() {
    std::wstring exe_path = get_executable_path();
    std::filesystem::path p(exe_path);

    // 获取可执行文件所在目录
    std::filesystem::path exe_dir = p.parent_path();

    // 构建图标路径
    std::filesystem::path icon_path = exe_dir / "amcl.dist" / "assets" / "img" / "logo" / "logo-256x.png";

    return icon_path.wstring();
}

bool initialize_wintoast() {
    if (!WinToast::isCompatible()) {
        return false;
    }

    WinToast::instance()->setAppName(L"AMCL");
    WinToast::instance()->setAppUserModelId(L"AMCL.App");

    return true;
}
#endif

void show_toast(const std::wstring title, const std::wstring message) {
#ifdef _WIN32
    WinToast::WinToastError error;
    if (!WinToast::isCompatible())
        std::wcout << L"Error, your system in not supported!" << std::endl;
    WinToast::instance()->setAppName(L"Astra Minecraft Launcher");
    WinToast::instance()->setShortcutPolicy(WinToast::SHORTCUT_POLICY_REQUIRE_CREATE);

    const auto appUserModelId = WinToast::configureAUMI(L"", L"Astra Minecraft Launcher", L"", L"");
    WinToast::instance()->setAppUserModelId(appUserModelId);

    if (!WinToast::instance()->initialize(&error))
        std::wcout << L"Error, could not initialize the lib!" << std::endl;

    MWinToastHandler* handler = new MWinToastHandler();
    WinToastTemplate templ = WinToastTemplate(WinToastTemplate::ImageAndText02);

    std::wstring icon_path = get_icon_path();

    if (std::filesystem::exists(icon_path)) {
        templ.setImagePath(icon_path);
    } else {
        std::wcout << L"Warning: Icon file not found at " << icon_path << std::endl;
        templ = WinToastTemplate(WinToastTemplate::Text02);
    }

    templ.setTextField(title, WinToastTemplate::FirstLine);
    templ.setTextField(message, WinToastTemplate::SecondLine);

    templ.setExpiration(3000);

    if (WinToast::instance()->showToast(templ, handler) < 0)
        std::wcout << L"Could not launch your toast notification!";

#elif __APPLE__
    std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
    std::string narrow_title = converter.to_bytes(title);
    std::string narrow_message = converter.to_bytes(message);

    std::string script = "display notification \"" + narrow_message + "\" with title \"" + narrow_title + "\"";
    system(("osascript -e '" + script + "'").c_str());
#else
    std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
    std::string narrow_title = converter.to_bytes(title);
    std::string narrow_message = converter.to_bytes(message);
    notify_init("AMCL");
    NotifyNotification* notification = notify_notification_new(narrow_title.c_str(), narrow_message.c_str(), nullptr);
    notify_notification_set_timeout(notification, 3000);
    notify_notification_show(notification, nullptr);
    g_object_unref(G_OBJECT(notification));
    notify_uninit();
#endif
}

void show_first_launch_toast()
{
    std::wstring title = i18n("toast_title");
    std::wstring message = i18n("toast_message");
    show_toast(title, message);
}

void show_error_message(const std::string& logPath) {
    std::wstring title = i18n("error_title");
    std::wstring format_str = i18n("error_message");

    std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
    std::string narrow_format = converter.to_bytes(format_str);

    size_t needed = snprintf(nullptr, 0, narrow_format.c_str(), logPath.c_str()) + 1;
    std::unique_ptr<char[]> buffer(new char[needed]);
    snprintf(buffer.get(), needed, narrow_format.c_str(), logPath.c_str());
    std::string narrow_msg(buffer.get());

    std::wstring msg = converter.from_bytes(narrow_msg);

    #ifdef _WIN32
        MessageBoxW(nullptr, msg.c_str(), title.c_str(), MB_OK | MB_ICONERROR);
    #elif __APPLE__
        std::string script = "display dialog \"" + narrow_msg +
                             "\" with title \"" + converter.to_bytes(title) +
                             "\" buttons {\"OK\"} default button \"OK\" with icon stop";
        system(("osascript -e '" + script + "'").c_str());
    #else
        std::string cmd = "zenity --error --title=\"" + converter.to_bytes(title) +
                          "\" --text=\"" + narrow_msg + "\"";
        system(cmd.c_str());
    #endif
}

void open_log_directory(const std::string& logPath) {
    #ifdef _WIN32
        std::string cmd = "explorer /select,\"" + logPath + "\"";
        system(cmd.c_str());
    #elif __APPLE__
        system(("open -R \"" + logPath + "\"").c_str());
    #else
        system(("xdg-open \"" + logPath + "\"").c_str());
    #endif
}

#ifdef _WIN32
int execute(const std::string& exe_path, const std::string& log_path)
{
    std::filesystem::path abs_path = std::filesystem::absolute(exe_path);
    abs_path += ".exe";

    if (!std::filesystem::exists(abs_path)) {
        std::ofstream log_file(log_path, std::ios::app);
        log_file << "Error: Executable not found at " << abs_path << std::endl;
        return -1;
    }

    std::string commandLine = "\"" + abs_path.string() + "\"";

    STARTUPINFOA si = { sizeof(STARTUPINFOA) };
    PROCESS_INFORMATION pi = { 0 };

    SECURITY_ATTRIBUTES sa = { sizeof(SECURITY_ATTRIBUTES) };
    sa.bInheritHandle = TRUE;
    sa.lpSecurityDescriptor = NULL;

    HANDLE hLog = CreateFileA(
        log_path.c_str(),
        FILE_APPEND_DATA,
        FILE_SHARE_READ,
        &sa,
        OPEN_ALWAYS,
        FILE_ATTRIBUTE_NORMAL,
        NULL
    );

    if (hLog == INVALID_HANDLE_VALUE) {
        return -1;
    }

    si.dwFlags |= STARTF_USESTDHANDLES;
    si.hStdOutput = hLog;
    si.hStdError = hLog;

    BOOL success = CreateProcessA(
        NULL,
        const_cast<char*>(commandLine.c_str()), // 命令行
        NULL,                   // 进程安全属性
        NULL,                   // 线程安全属性
        TRUE,                   // 继承句柄
        CREATE_NO_WINDOW,       // 创建标志：不创建控制台窗口
        NULL,                   // 环境块
        NULL,                   // 当前目录
        &si,                    // 启动信息
        &pi                     // 进程信息
    );

    CloseHandle(hLog);

    if (!success) {
        DWORD error = GetLastError();
        std::ofstream log_file(log_path, std::ios::app);
        log_file << "Error: Failed to create process. Error code: " << error << std::endl;
        return -1;
    }

    WaitForSingleObject(pi.hProcess, INFINITE);

    DWORD exitCode;
    GetExitCodeProcess(pi.hProcess, &exitCode);

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return (int)exitCode;
}
#else
int execute(const std::string& exe_path, const std::string& log_path)
{
    std::filesystem::path abs_path = std::filesystem::absolute(exe_path);

    if (!std::filesystem::exists(abs_path)) {
        std::ofstream log_file(log_path, std::ios::app);
        log_file << "Error: Executable not found at " << abs_path << std::endl;
        return -1;
    }

    std::string command = abs_path.string() + " 2>&1";

    FILE* pipe = popen(command.c_str(), "r");
    if (!pipe) {
        std::ofstream log_file(log_path, std::ios::app);
        log_file << "Error: Failed to execute command: " << command << std::endl;
        return -1;
    }

    std::ofstream log_file(log_path);
    char buffer[128];

    while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
        log_file << buffer;
    }

    int status = pclose(pipe);
    return WEXITSTATUS(status);
}
#endif