#include <windows.h>
#include <fwpmu.h>
#include <tlhelp32.h>
#include <iostream>

#pragma comment(lib, "Fwpuclnt.lib")
BYTE* GetProcessAppId(DWORD processId, DWORD* appIdSize) {
    HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, processId);
    if (!hProcess) {
        return NULL;
    }

    HANDLE hToken = NULL;
    if (!OpenProcessToken(hProcess, TOKEN_QUERY, &hToken)) {
        CloseHandle(hProcess);
        return NULL;
    }

    DWORD size = 0;
    GetTokenInformation(hToken, TokenUser, NULL, 0, &size);
    BYTE* sid = new BYTE[size];
    if (GetTokenInformation(hToken, TokenUser, sid, size, &size)) {
        *appIdSize = size;
    }
    else {
        delete[] sid;
        sid = NULL;
    }

    CloseHandle(hToken);
    CloseHandle(hProcess);
    return sid;
}
DWORD GetProcessIdByName(const wchar_t* processName) {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) {
        return 0;
    }

    PROCESSENTRY32 entry;
    entry.dwSize = sizeof(PROCESSENTRY32);

    if (Process32First(snapshot, &entry)) {
        do {
            if (_wcsicmp(entry.szExeFile, processName) == 0) {
                CloseHandle(snapshot);
                return entry.th32ProcessID;
            }
        } while (Process32Next(snapshot, &entry));
    }

    CloseHandle(snapshot);
    return 0;
}

int main() {
    HANDLE engineHandle = NULL;
    FWPM_SESSION0 session = { 0 };
    session.displayData.name = const_cast<wchar_t*>(L"WFP Session");
    DWORD result = FwpmEngineOpen0(NULL, RPC_C_AUTHN_WINNT, NULL, &session, &engineHandle);
    if (result != ERROR_SUCCESS) {
        std::wcout << L"Failed to open WFP engine: " << result << std::endl;
        return -1;
    }
    const wchar_t* processes[] = { L"MsMpEng.exe", L"MsSense.exe" };
    size_t processCount = sizeof(processes) / sizeof(processes[0]);
    for (size_t i = 0; i < processCount; ++i) {
        DWORD processId = GetProcessIdByName(processes[i]);
        if (processId == 0) {
            std::wcout << L"Failed to find process: " << processes[i] << std::endl;
            continue;
        }

        DWORD appIdSize = 0;
        BYTE* appId = GetProcessAppId(processId, &appIdSize);
        if (appId == NULL) {
            std::wcout << L"Failed to get App ID for process: " << processes[i] << std::endl;
            continue;
        }
        FWPM_FILTER_CONDITION0 condition = { 0 };
        condition.fieldKey = FWPM_CONDITION_ALE_APP_ID;
        condition.matchType = FWP_MATCH_EQUAL;

        FWP_BYTE_BLOB byteBlob = { 0 };
        byteBlob.size = appIdSize;
        byteBlob.data = appId;
        condition.conditionValue.type = FWP_BYTE_BLOB_TYPE;
        condition.conditionValue.byteBlob = &byteBlob;
        FWPM_FILTER0 filter = { 0 };
        filter.layerKey = FWPM_LAYER_ALE_AUTH_CONNECT_V4;
        filter.displayData.name = const_cast<wchar_t*>(L"Block Network Activity"); // Use const_cast

        filter.action.type = FWP_ACTION_BLOCK;
        filter.numFilterConditions = 1;
        filter.filterCondition = &condition;

        result = FwpmFilterAdd0(engineHandle, &filter, NULL, NULL);
        if (result != ERROR_SUCCESS) {
            std::wcout << L"Failed to add filter for process: " << processes[i] << L" Error: " << result << std::endl;
        }
        else {
            std::wcout << L"Successfully added filter for process: " << processes[i] << std::endl;
        }

        delete[] appId;
    }

    FwpmEngineClose0(engineHandle);
    return 0;
}
