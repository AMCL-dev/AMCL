#include <iostream>
#include <fstream>
#include <filesystem>
#include <string>
#include <chrono>
#include <ctime>
#include "platform.h"

#ifdef _WIN32
    #include <windows.h>
    #define WEXITSTATUS(status) (status)
#else
    #include <cstdio>
    #include <unistd.h>
#endif

namespace fs = std::filesystem;

std::string get_timestamp()
{
    auto now = std::chrono::system_clock::now();
    auto time_t = std::chrono::system_clock::to_time_t(now);
    std::tm tm = *std::localtime(&time_t);
    char buffer[20];
    strftime(buffer, sizeof(buffer), "%Y%m%d%H%M%S", &tm);
    return std::string(buffer);
}

fs::path get_home_dir()
{
    #ifdef _WIN32
        const char* home = std::getenv("USERPROFILE");
    #else
        const char* home = std::getenv("HOME");
    #endif
    return home ? fs::path(home) : fs::current_path();
}

fs::path get_amcl_dir()
{
    return get_home_dir() / ".amcl";
}

void ensure_directories()
{
    auto amcl_dir = get_amcl_dir();
    auto logs_dir = amcl_dir / "logs";

    if (!fs::exists(amcl_dir)) fs::create_directory(amcl_dir);
    if (!fs::exists(logs_dir)) fs::create_directory(logs_dir);
}

bool is_first_launch()
{
    auto flag_file = get_amcl_dir() / "firststart";
    if (!fs::exists(flag_file)) {
        std::ofstream file(flag_file);
        file << "false";
        file.close();
        return true;
    }
    return false;
}

#ifdef _WIN32
int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PWSTR pCmdLine, int nCmdShow)
#else
int main()
#endif
{
    try {
        ensure_directories();

        if (is_first_launch()) {
            show_first_launch_toast();
        }

        std::string log_file = (get_amcl_dir() / "logs" /
                              ("launcher_log_" + get_timestamp() + ".log")).string();

        int exit_code = execute("./amcl.dist/amcl", log_file);

        if (exit_code != 0) {
            show_error_message(log_file);
            open_log_directory(log_file);
            return 1;
        }

        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Critical error: " << e.what() << std::endl;
        return 1;
    }
}