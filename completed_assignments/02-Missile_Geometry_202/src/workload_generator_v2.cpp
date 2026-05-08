#include <algorithm>
#include <fstream>
#include <functional>
#include <iomanip>
#include <iostream>
#include <optional>
#include <random>
#include <string>
#include <unordered_map>
#include <vector>

#include "json.hpp"
#include "termcolor.hpp"
#include "usagePrinter.hpp"

using json = nlohmann::json;

// -------------------------------------------------------------
// Unified operation record
// -------------------------------------------------------------
// Project 1 (set/dictionary) uses:
//   insert / contains / delete   with a value
//
// Project 2 (priority queue) uses:
//   push  with priority + value
//   peek  with no payload
//   pop   with no payload
//
// We keep one JSON shape and only emit fields that are present.
struct Op {
    std::string op;
    std::optional<int> value;
    std::optional<int> priority;
};

void to_json(json& j, const Op& o) {
    j = json{{"op", o.op}};

    if (o.value.has_value()) {
        j["value"] = *o.value;
    }

    if (o.priority.has_value()) {
        j["priority"] = *o.priority;
    }
}

// -------------------------------------------------------------
// Workload generator
// -------------------------------------------------------------
class WorkloadGenerator {
private:
    int seed;
    int valueRangeMult;

    std::mt19937 rng() const {
        return std::mt19937(seed);
    }

    std::vector<int> genValues(int n, int count) const {
        std::mt19937 r = rng();
        int hi = std::max(1, valueRangeMult * n);
        std::uniform_int_distribution<int> dist(0, hi);

        std::vector<int> values;
        values.reserve(count);

        for (int i = 0; i < count; i++) {
            values.push_back(dist(r));
        }

        return values;
    }

    std::vector<int> genPriorities(int n, int count) const {
        std::mt19937 r(seed + 17);
        int hi = std::max(1, n / 2);
        std::uniform_int_distribution<int> dist(0, hi);

        std::vector<int> values;
        values.reserve(count);

        for (int i = 0; i < count; i++) {
            values.push_back(dist(r));
        }

        return values;
    }

public:
    WorkloadGenerator(int seed_ = 42, int valueRangeMult_ = 10)
        : seed(seed_), valueRangeMult(valueRangeMult_) {}

    // ---------------------------------------------------------
    // Project 1: set / dictionary workloads
    // ---------------------------------------------------------
    std::vector<Op> setWorkloadA(int n) const {
        auto inserts = genValues(n, n);
        auto lookups = genValues(n, n);

        std::vector<Op> ops;
        ops.reserve(2 * n);

        for (int x : inserts) {
            ops.push_back({"insert", x, std::nullopt});
        }

        for (int x : lookups) {
            ops.push_back({"contains", x, std::nullopt});
        }

        return ops;
    }

    std::vector<Op> setWorkloadB(int n) const {
        auto inserts = genValues(n, n);
        std::sort(inserts.begin(), inserts.end());

        auto lookups = genValues(n, n);

        std::vector<Op> ops;
        ops.reserve(2 * n);

        for (int x : inserts) {
            ops.push_back({"insert", x, std::nullopt});
        }

        for (int x : lookups) {
            ops.push_back({"contains", x, std::nullopt});
        }

        return ops;
    }

    std::vector<Op> setWorkloadC(int n) const {
        std::mt19937 r = rng();
        int hi = std::max(1, valueRangeMult * n);
        std::uniform_int_distribution<int> dist(0, hi);

        int totalOps = 2 * n;
        int numContains = totalOps / 2;
        int numInsert = totalOps / 4;
        int numDelete = totalOps - numContains - numInsert;

        std::vector<std::string> opTypes;
        opTypes.reserve(totalOps);
        opTypes.insert(opTypes.end(), numContains, "contains");
        opTypes.insert(opTypes.end(), numInsert, "insert");
        opTypes.insert(opTypes.end(), numDelete, "delete");
        std::shuffle(opTypes.begin(), opTypes.end(), r);

        std::vector<Op> ops;
        ops.reserve(totalOps);
        std::vector<int> population;
        population.reserve(n);

        for (const auto& op : opTypes) {
            int x = dist(r);

            if (op == "insert") {
                population.push_back(x);
                ops.push_back({"insert", x, std::nullopt});
            } else if (op == "contains") {
                ops.push_back({"contains", x, std::nullopt});
            } else {
                if (!population.empty()) {
                    int y = population.back();
                    population.pop_back();
                    ops.push_back({"delete", y, std::nullopt});
                } else {
                    ops.push_back({"contains", x, std::nullopt});
                }
            }
        }

        return ops;
    }

    std::vector<Op> setWorkloadD(int n) const {
        auto inserts = genValues(n, n);
        auto lookups = genValues(n, 5 * n);

        std::vector<Op> ops;
        ops.reserve(6 * n);

        for (int x : inserts) {
            ops.push_back({"insert", x, std::nullopt});
        }

        for (int x : lookups) {
            ops.push_back({"contains", x, std::nullopt});
        }

        return ops;
    }

    // ---------------------------------------------------------
    // Project 2: priority queue workloads
    // ---------------------------------------------------------
    // A: bulk push then drain with pop
    std::vector<Op> pqWorkloadA(int n) const {
        auto priorities = genPriorities(n, n);
        auto values = genValues(n, n);

        std::vector<Op> ops;
        ops.reserve(2 * n);

        for (int i = 0; i < n; i++) {
            ops.push_back({"push", values[i], priorities[i]});
        }

        for (int i = 0; i < n; i++) {
            ops.push_back({"pop", std::nullopt, std::nullopt});
        }

        return ops;
    }

    // B: sorted-priority pushes then drain
    std::vector<Op> pqWorkloadB(int n) const {
        auto priorities = genPriorities(n, n);
        auto values = genValues(n, n);
        std::sort(priorities.begin(), priorities.end());

        std::vector<Op> ops;
        ops.reserve(2 * n);

        for (int i = 0; i < n; i++) {
            ops.push_back({"push", values[i], priorities[i]});
        }

        for (int i = 0; i < n; i++) {
            ops.push_back({"pop", std::nullopt, std::nullopt});
        }

        return ops;
    }

    // C: mixed live queue
    // 50% peek, 30% push, 20% pop. Empty queue falls back to push.
    std::vector<Op> pqWorkloadC(int n) const {
        std::mt19937 r = rng();
        int totalOps = 3 * n;
        int numPeek = (totalOps * 50) / 100;
        int numPush = (totalOps * 30) / 100;
        int numPop = totalOps - numPeek - numPush;

        int hiValue = std::max(1, valueRangeMult * n);
        int hiPriority = std::max(1, n / 2);
        std::uniform_int_distribution<int> valueDist(0, hiValue);
        std::uniform_int_distribution<int> priorityDist(0, hiPriority);

        std::vector<std::string> opTypes;
        opTypes.reserve(totalOps);
        opTypes.insert(opTypes.end(), numPeek, "peek");
        opTypes.insert(opTypes.end(), numPush, "push");
        opTypes.insert(opTypes.end(), numPop, "pop");
        std::shuffle(opTypes.begin(), opTypes.end(), r);

        std::vector<Op> ops;
        ops.reserve(totalOps);
        int currentSize = 0;

        for (const auto& op : opTypes) {
            if (op == "push") {
                ops.push_back({"push", valueDist(r), priorityDist(r)});
                currentSize++;
            } else if (op == "peek") {
                if (currentSize > 0) {
                    ops.push_back({"peek", std::nullopt, std::nullopt});
                } else {
                    ops.push_back({"push", valueDist(r), priorityDist(r)});
                    currentSize++;
                }
            } else {
                if (currentSize > 0) {
                    ops.push_back({"pop", std::nullopt, std::nullopt});
                    currentSize--;
                } else {
                    ops.push_back({"push", valueDist(r), priorityDist(r)});
                    currentSize++;
                }
            }
        }

        return ops;
    }

    // D: build once, then steady-state service
    // n pushes, then 2n cycles of peek/pop/push to keep queue alive
    std::vector<Op> pqWorkloadD(int n) const {
        std::mt19937 r = rng();
        int hiValue = std::max(1, valueRangeMult * n);
        int hiPriority = std::max(1, n / 2);
        std::uniform_int_distribution<int> valueDist(0, hiValue);
        std::uniform_int_distribution<int> priorityDist(0, hiPriority);

        std::vector<Op> ops;
        ops.reserve(7 * n);

        for (int i = 0; i < n; i++) {
            ops.push_back({"push", valueDist(r), priorityDist(r)});
        }

        for (int i = 0; i < 2 * n; i++) {
            ops.push_back({"peek", std::nullopt, std::nullopt});
            ops.push_back({"pop", std::nullopt, std::nullopt});
            ops.push_back({"push", valueDist(r), priorityDist(r)});
        }

        return ops;
    }
};

struct Args {
    std::string mode = "set";      // set | pq
    std::string workload = "A";    // A | B | C | D
    int size = 10;
    int preview = 20;
    bool emitJson = false;
    std::string savefile = "";

    friend std::ostream& operator<<(std::ostream& os, const Args& a) {
        return os << "[mode:" << a.mode
                  << ", workload:" << a.workload
                  << ", size:" << a.size
                  << ", preview:" << a.preview
                  << ", json:" << a.emitJson
                  << ", save:" << a.savefile << "]";
    }
};

Args parseArgs(int argc, char* argv[]) {
    Args args;

    for (int i = 1; i < argc; i++) {
        std::string s = argv[i];

        if ((s == "-m" || s == "--mode") && i + 1 < argc) {
            args.mode = argv[++i];
        } else if ((s == "-w" || s == "--workload") && i + 1 < argc) {
            args.workload = argv[++i];
        } else if ((s == "-n" || s == "--size") && i + 1 < argc) {
            args.size = std::stoi(argv[++i]);
        } else if ((s == "-p" || s == "--preview") && i + 1 < argc) {
            args.preview = std::stoi(argv[++i]);
        } else if (s == "--json") {
            args.emitJson = true;
        } else if ((s == "-s" || s == "--save") && i + 1 < argc) {
            args.savefile = argv[++i];
        } else if (s == "-h" || s == "--help") {
            UsagePrinter help;
            help.add("-m, --mode", "<set|pq>", "Generator family: set (Project 1) or pq (Project 2)");
            help.add("-w, --workload", "<A|B|C|D>", "Workload type");
            help.add("-n, --size", "<N>", "Base problem size");
            help.add("-p, --preview", "<K>", "Preview first K operations");
            help.add("--json", "", "Emit JSON to stdout");
            help.add("-s, --save", "<FILENAME>", "Save prettified JSON to a file");
            help.addExample("./workload_generator --mode set -w C -n 1000 --json > set_C_1000.json");
            help.addExample("./workload_generator --mode pq  -w B -n 1000 --json > pq_B_1000.json");
            help.addExample("./workload_generator --mode pq -w D -n 25 --preview 20");
            help.print("workload_generator");
            std::exit(0);
        }
    }

    return args;
}

template <typename T>
void emitJson(const T& ops) {
    json j = ops;
    std::cout << j.dump(2) << "\n";
}

int main(int argc, char* argv[]) {
    Args args = parseArgs(argc, argv);
    WorkloadGenerator gen(42);

    std::unordered_map<std::string, std::function<std::vector<Op>(int)>> workloads;

    if (args.mode == "set") {
        workloads = {
            {"A", [&](int n) { return gen.setWorkloadA(n); }},
            {"B", [&](int n) { return gen.setWorkloadB(n); }},
            {"C", [&](int n) { return gen.setWorkloadC(n); }},
            {"D", [&](int n) { return gen.setWorkloadD(n); }},
        };
    } else if (args.mode == "pq") {
        workloads = {
            {"A", [&](int n) { return gen.pqWorkloadA(n); }},
            {"B", [&](int n) { return gen.pqWorkloadB(n); }},
            {"C", [&](int n) { return gen.pqWorkloadC(n); }},
            {"D", [&](int n) { return gen.pqWorkloadD(n); }},
        };
    } else {
        std::cerr << "Error: mode must be 'set' or 'pq'.\n";
        return 1;
    }

    if (workloads.find(args.workload) == workloads.end()) {
        std::cerr << "Error: workload must be one of A, B, C, D.\n";
        return 1;
    }

    auto ops = workloads[args.workload](args.size);

    if (args.emitJson) {
        emitJson(ops);
    }

    if (args.preview > 0 && args.savefile.empty()) {
        std::cout << "\n----------------------------------\n";
        std::cout << "Mode: " << args.mode << "\n";
        std::cout << "Workload: " << args.workload << "\n";
        std::cout << "n: " << args.size << "\n";
        std::cout << "Total operations: " << ops.size() << "\n";
        std::cout << "----------------------------------\n\n";

        int previewCount = std::min<int>(args.preview, static_cast<int>(ops.size()));

        for (int i = 0; i < previewCount; i++) {
            json j = ops[i];
            std::cout << j.dump() << "\n";
        }

        if (previewCount < static_cast<int>(ops.size())) {
            std::cout << "...\n";
        }
    }

    if (!args.savefile.empty()) {
        std::cout << "Saving json to: " << args.savefile << "\n";
        json j = ops;
        std::ofstream out(args.savefile);
        out << std::setw(4) << j << std::endl;
    }

    return 0;
}
