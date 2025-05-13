#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <chrono>
#include <map>
#include <sys/resource.h>
#include <cctype>

const int GAP_PENALTY = 30;

std::map<std::pair<char, char>, int> ALPHA = {
    {{'A', 'A'}, 0}, {{'A', 'C'}, 110}, {{'A', 'G'}, 48}, {{'A', 'T'}, 94},
    {{'C', 'A'}, 110}, {{'C', 'C'}, 0}, {{'C', 'G'}, 118}, {{'C', 'T'}, 48},
    {{'G', 'A'}, 48}, {{'G', 'C'}, 118}, {{'G', 'G'}, 0}, {{'G', 'T'}, 110},
    {{'T', 'A'}, 94}, {{'T', 'C'}, 48}, {{'T', 'G'}, 110}, {{'T', 'T'}, 0}
};

long getMemoryUsageKB() {
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);
    return usage.ru_maxrss;
}

std::string generateString(const std::string& baseString, const std::vector<int>& indices) {
    std::string result = baseString;
    for (int index : indices) {
        if (index < 0 || index + 1 > result.length()) {
            std::cerr << "Invalid index " << index << " for string of length " << result.length() << ". Skipping.\n";
            continue;
        }
        result = result.substr(0, index + 1) + result + result.substr(index + 1);
    }
    return result;
}

std::pair<std::string, std::string> parseInputFile(const std::string& filePath) {
    std::ifstream file(filePath);
    if (!file.is_open()) {
        std::cerr << "Error: Cannot open input file " << filePath << std::endl;
        exit(1);
    }

    std::string baseString1, baseString2, line;
    std::vector<int> indices1, indices2;

    std::getline(file, baseString1);
    baseString1.erase(remove_if(baseString1.begin(), baseString1.end(), ::isspace), baseString1.end());

    while (std::getline(file, line)) {
        line.erase(remove_if(line.begin(), line.end(), ::isspace), line.end());
        if (line.empty()) continue;
        if (std::all_of(line.begin(), line.end(), ::isdigit)) {
            indices1.push_back(std::stoi(line));
        } else {
            baseString2 = line;
            break;
        }
    }

    baseString2.erase(remove_if(baseString2.begin(), baseString2.end(), ::isspace), baseString2.end());

    while (std::getline(file, line)) {
        line.erase(remove_if(line.begin(), line.end(), ::isspace), line.end());
        if (line.empty()) continue;
        if (std::all_of(line.begin(), line.end(), ::isdigit)) {
            indices2.push_back(std::stoi(line));
        } else {
            std::cerr << "Unexpected non-digit line: " << line << std::endl;
            exit(1);
        }
    }

    std::string string1 = generateString(baseString1, indices1);
    std::string string2 = generateString(baseString2, indices2);
    return {string1, string2};
}

std::tuple<int, std::string, std::string> alignStrings(const std::string& X, const std::string& Y) {
    int m = X.length(), n = Y.length();
    std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1));

    for (int i = 0; i <= m; ++i) dp[i][0] = i * GAP_PENALTY;
    for (int j = 0; j <= n; ++j) dp[0][j] = j * GAP_PENALTY;

    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            int match = dp[i-1][j-1] + ALPHA[{X[i-1], Y[j-1]}];
            int gap1 = dp[i][j-1] + GAP_PENALTY;
            int gap2 = dp[i-1][j] + GAP_PENALTY;
            dp[i][j] = std::min({match, gap1, gap2});
        }
    }

    std::string alignedX = "", alignedY = "";
    int i = m, j = n;
    while (i > 0 || j > 0) {
        if (i > 0 && j > 0 && dp[i][j] == dp[i-1][j-1] + ALPHA[{X[i-1], Y[j-1]}]) {
            alignedX = X[i-1] + alignedX;
            alignedY = Y[j-1] + alignedY;
            i--; j--;
        } else if (j > 0 && dp[i][j] == dp[i][j-1] + GAP_PENALTY) {
            alignedX = '_' + alignedX;
            alignedY = Y[j-1] + alignedY;
            j--;
        } else {
            alignedX = X[i-1] + alignedX;
            alignedY = '_' + alignedY;
            i--;
        }
    }
    return {dp[m][n], alignedX, alignedY};
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: ./basic <input_file> <output_file>\n";
        return 1;
    }

    std::string inputFile = argv[1];
    std::string outputFile = argv[2];

    long memoryBefore = getMemoryUsageKB();
    auto start = std::chrono::high_resolution_clock::now();

    auto [X, Y] = parseInputFile(inputFile);
    auto [cost, alignedX, alignedY] = alignStrings(X, Y);

    auto end = std::chrono::high_resolution_clock::now();
    long memoryAfter = getMemoryUsageKB();
    std::chrono::duration<double, std::milli> elapsed = end - start;

    std::ofstream out(outputFile);
    if (!out.is_open()) {
        std::cerr << "Error: Cannot open output file " << outputFile << std::endl;
        return 1;
    }

    out << cost << "\n";
    out << alignedX << "\n";
    out << alignedY << "\n";
    out << elapsed.count() << "\n";
    out << (memoryAfter - memoryBefore) << "\n";

    return 0;
}