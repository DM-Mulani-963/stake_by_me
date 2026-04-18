# Stake By Me - CLI Tool

Simple standalone CLI for complete registration automation - **no Docker required!**

## 🚀 Quick Start

```bash
# 1. Check dependencies
python3 cli/stake_cli.py check

# 2. Install Playwright browsers (first time only)
python3 cli/stake_cli.py install-playwright

# 3. Process data (JSON → Excel)
python3 cli/stake_cli.py process

# 4. Run complete workflow
python3 cli/stake_cli.py run

# 5. Test browser (visible window)
python3 cli/stake_cli.py test-browser --no-headless
```

## 📋 Commands

| Command              | Description                                |
| -------------------- | ------------------------------------------ |
| `check`              | Check all dependencies                     |
| `install-playwright` | Install Playwright browsers                |
| `process`            | Process JSON → Excel only                  |
| `run`                | Complete workflow (process + register all) |
| `test-browser`       | Test browser automation                    |

## 🎯 Options

- `--no-headless` - Show browser window (useful for debugging)

## 📂 File Locations

- **Input**: `input/*.json` - Place your JSON data files here
- **Output**: `output/*.xlsx` - Generated Excel files
- **Screenshots**: `screenshots/` - Verification screenshots
- **Logs**: `cli/stake_cli.log` - Execution logs

## 💡 Examples

### Process Data Only

```bash
python3 cli/stake_cli.py process
```

### Run with Visible Browser

```bash
python3 cli/stake_cli.py run --no-headless
```

### Complete Workflow (Headless)

```bash
python3 cli/stake_cli.py run
```

## 🔧 Troubleshooting

### Missing Dependencies

```bash
pip install -r requirements.txt
python3 cli/stake_cli.py check
```

### Playwright Issues

```bash
python3 cli/stake_cli.py install-playwright
```

### View Logs

```bash
tail -f cli/stake_cli.log
```

## ✨ Features

- ✅ No Docker required
- ✅ Single command execution
- ✅ Progress tracking
- ✅ Detailed logging
- ✅ Summary statistics
- ✅ Error handling
- ✅ Screenshot capture
