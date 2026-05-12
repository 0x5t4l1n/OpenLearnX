# Supported Programming Languages

## OpenLearnX Compiler Service - Language Support

The code execution platform now supports **20+ programming languages** with comprehensive security sandboxing.

---

## ✅ **Supported Languages**

### **Interpreted Languages (Runtime)**
| Language | Alias | Timeout | Memory | Command | Version |
|----------|-------|---------|--------|---------|---------|
| **Python** | `py` | 8s | 128MB | `python /workspace/code.py` | 3.11-alpine |
| **JavaScript** | `js` | 8s | 128MB | `node /workspace/code.js` | 20-alpine |
| **Bash/Shell** | `bash`, `sh` | 10s | 64MB | `bash /workspace/code.sh` | 5-alpine |
| **Ruby** | `rb` | 10s | 128MB | `ruby /workspace/code.rb` | 3.2-alpine |
| **PHP** | `php` | 8s | 128MB | `php /workspace/code.php` | 8.2-alpine |
| **Lua** | `lua` | 8s | 64MB | `lua /workspace/code.lua` | 5.4 |
| **Perl** | `pl` | 10s | 128MB | `perl /workspace/code.pl` | 5.36-alpine |
| **R** | `r` | 15s | 256MB | `Rscript /workspace/code.R` | latest |
| **Julia** | `julia` | 15s | 256MB | `julia /workspace/code.jl` | 1.9-alpine |

### **Compiled Languages (Compiled)**
| Language | Alias | Timeout | Memory | Compiler | Runtime |
|----------|-------|---------|--------|----------|---------|
| **C** | `c` | 10s | 192MB | `gcc -O2` | `./program` |
| **C++** | `cpp`, `c++` | 10s | 256MB | `g++ -std=c++17` | `./program` |
| **Java** | `java` | 12s | 256MB | `javac` | `java -cp` |
| **Go** | `go` | 14s | 256MB | `go build` | `./program` |
| **Rust** | `rust` | 20s | 512MB | `rustc -O` | `./program` |
| **Kotlin** | `kt` | 15s | 256MB | `kotlinc` | `java -jar` |
| **Swift** | `swift` | 15s | 256MB | `swiftc -O` | `./program` |
| **TypeScript** | `ts` | 10s | 256MB | `tsc` | `node` |
| **C#** | `cs`, `csharp` | 15s | 512MB | `dotnet build` | `dotnet` |
| **Scala** | `scala` | 15s | 256MB | `scalac` | `scala` |
| **Groovy** | `groovy` | 12s | 256MB | `groovy` | `groovy` |

---

## 🔧 **API Usage Examples**

### **Execute Python**
```bash
curl -X POST http://localhost:5000/api/compiler/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(\"Hello World\")"
  }'
```

### **Execute JavaScript**
```bash
curl -X POST http://localhost:5000/api/compiler/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "javascript",
    "code": "console.log(\"Hello World\")"
  }'
```

### **Execute Java**
```bash
curl -X POST http://localhost:5000/api/compiler/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "java",
    "code": "public class Main { public static void main(String[] args) { System.out.println(\"Hello World\"); } }"
  }'
```

### **Execute with Input Data**
```bash
curl -X POST http://localhost:5000/api/compiler/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "x = input(); print(int(x) * 2)",
    "input": "5"
  }'
```

### **Execute Bash Script**
```bash
curl -X POST http://localhost:5000/api/compiler/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "bash",
    "code": "#!/bin/bash\necho \"Hello from Bash\"\necho \"Current date: $(date)\""
  }'
```

### **Execute with Aliases**
```bash
# Using short alias
curl -X POST http://localhost:5000/api/compiler/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "py",
    "code": "print(\"Python via py alias\")"
  }'

# Using c++ alias
curl -X POST http://localhost:5000/api/compiler/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "c++",
    "code": "#include <iostream>\nint main() { std::cout << \"Hello C++\"; return 0; }"
  }'
```

---

## 🔒 **Security Features**

### **Sandbox Isolation**
- ✅ Docker containerization for each execution
- ✅ Memory limits (64MB - 512MB per language)
- ✅ CPU limits (0.25 - 0.8 cores)
- ✅ Timeout protection (8s - 20s)
- ✅ Read-only filesystem

### **Blocked Operations**
Each language has specific restricted operations:

**Python:**
- `os`, `socket`, `subprocess` modules
- `eval()`, `exec()`, `__import__()`
- File I/O operations

**JavaScript:**
- `child_process` module
- `process.env`, `process.binding`
- File system access

**Bash:**
- Command substitution patterns
- `/dev` access
- Dangerous commands (`rm -rf`, `dd`)

**Java:**
- `Runtime.getRuntime()`
- `ProcessBuilder`
- Network operations (`java.net`)

**C/C++:**
- `system()`, `popen()`, `fork()`
- Socket operations
- File operations

**Go:**
- `exec.Command()`
- Network access
- File operations

**Rust:**
- `std::process::Command`
- Network operations
- Unsafe blocks (when code is not in library context)

---

## 📊 **Language Statistics**

```
Total Languages Supported: 20
Interpreted Languages: 9
Compiled Languages: 11

Performance Tiers:
  Fast (8-10s):    Python, JavaScript, PHP, Lua, Bash (5 languages)
  Standard (10-15s): Ruby, C, C++, Java, Kotlin, Swift, TypeScript, Groovy (8 languages)
  Intensive (15-20s): Go, Rust, R, Julia, C#, Scala (6 languages)
```

---

## 🚀 **Getting Started with Each Language**

### **1. Python**
```python
# Your code here
print("Hello World")
name = input()
print(f"Hello {name}")
```

### **2. JavaScript**
```javascript
// Your code here
console.log("Hello World");
const name = "Alice";
console.log(`Hello ${name}`);
```

### **3. Bash**
```bash
#!/bin/bash
echo "Hello World"
echo "Current directory: $(pwd)"
```

### **4. Java**
```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
```

### **5. C++**
```cpp
#include <iostream>
int main() {
    std::cout << "Hello World" << std::endl;
    return 0;
}
```

### **6. Rust**
```rust
fn main() {
    println!("Hello World");
}
```

### **7. Go**
```go
package main
import "fmt"
func main() {
    fmt.Println("Hello World")
}
```

### **8. R**
```r
# Your code here
print("Hello World")
x <- c(1, 2, 3)
print(mean(x))
```

### **9. Ruby**
```ruby
puts "Hello World"
name = gets.chomp
puts "Hello #{name}"
```

---

## 📝 **API Response Format**

```json
{
  "success": true,
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "language": "python",
  "output": "Hello World\n",
  "error": "",
  "exit_code": 0,
  "execution_time": 0.245,
  "memory_used": 12.5,
  "timestamp": "2026-05-12T20:30:00.000Z"
}
```

---

## 🔧 **Configuration Details**

### **Docker Images Used**
- Python: `python:3.11-alpine`
- Node.js: `node:20-alpine`
- GCC/G++: `gcc:13`
- Java: `openjdk:17-alpine`
- Go: `golang:1.22-alpine`
- Rust: `rust:1.77-alpine`
- R: `rocker/r-base:latest`
- Julia: `julia:1.9-alpine`
- Ruby: `ruby:3.2-alpine`
- PHP: `php:8.2-alpine`
- Swift: `swift:5.9-alpine`
- C#/.NET: `mcr.microsoft.com/dotnet/sdk:7.0-alpine`

---

## ⚠️ **Limitations**

1. **Network Access**: Disabled for all languages (no external API calls)
2. **File I/O**: Limited to `/workspace` directory (read-only for most operations)
3. **Process Creation**: Disabled for security reasons
4. **Execution Time**: Maximum 20 seconds per execution
5. **Code Size**: Maximum 20,000 characters
6. **Memory**: Limited per language (64MB - 512MB)
7. **CPU**: Limited per language (0.25 - 0.8 cores)

---

## 🔄 **Adding New Languages**

To add a new language:

1. **Add configuration** in `language_configs` dict:
```python
"newlang": {
    "image": "newlang:version",
    "file_name": "code.ext",
    "compile_command": "compile command or None",
    "run_command": "run command",
    "timeout": 10,
    "memory_limit": "256m",
    "cpu_limit": 0.5,
}
```

2. **Add security patterns** in `blocked_patterns` dict:
```python
"newlang": [
    r"forbidden_pattern_1",
    r"forbidden_pattern_2",
]
```

3. **Add language aliases** (optional) in `execute_code()` method

---

## 📞 **Support & Troubleshooting**

**Issue**: Language not supported
- **Solution**: Check supported languages list above

**Issue**: Execution timeout
- **Solution**: Optimize code performance or increase timeout

**Issue**: Security violation
- **Solution**: Remove blocked operations (network, file I/O, process execution)

**Issue**: Memory limit exceeded
- **Solution**: Reduce data processing or optimize algorithms

---

## 📚 **References**

- Docker Images: https://hub.docker.com
- Language Documentation:
  - Python: https://docs.python.org
  - JavaScript: https://developer.mozilla.org
  - Java: https://docs.oracle.com/javase
  - C++: https://en.cppreference.com
  - Rust: https://doc.rust-lang.org
  - Go: https://golang.org/doc
  - Ruby: https://ruby-doc.org
  - R: https://www.r-project.org

---

**Last Updated**: May 12, 2026
**Version**: 2.0 (Multi-Language Support)
