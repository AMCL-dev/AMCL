#pragma once
#include <map>
#include <string>

#ifdef _WIN32
#define WEXITSTATUS(x) (x)
#endif

std::wstring i18n(const std::string &key);

void show_first_launch_toast();
void show_toast(std::wstring title, std::wstring message);

void show_error_message(const std::string& logPath);

void open_log_directory(const std::string& logPath);

int execute(const std::string& exe_path, const std::string& log_path);