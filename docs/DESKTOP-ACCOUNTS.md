# Several desktop instances, one per Claude account

## TLDR/BLUF

Run several Claude Desktop windows on one Windows login, each signed in to a different Claude
account. Give each account a shortcut that uses its own profile directory.

Each instance has its own sign-in and usage pool, so work can continue when one pool runs out. Each
config root also needs its own hooks.

Use this setup when you need several accounts. Profiles under one Windows login do not provide a
security boundary.

Copy [the launcher](#the-launcher-and-the-one-line-that-is-load-bearing) for each account, create
its shortcut, and sign in. Use [these checks](#check-it-on-your-own-machine) to confirm the profile
and config root.

---

## Why a second instance normally does nothing

Claude Desktop is an Electron application, installed by Squirrel under `%LOCALAPPDATA%`:

<!-- no-copy -->
```
%LOCALAPPDATA%\AnthropicClaude\app-<version>\claude.exe <- the real binary, version in the path
%LOCALAPPDATA%\AnthropicClaude\claude.exe               <- stub launcher, NOT always present
%LOCALAPPDATA%\AnthropicClaude\Update.exe               <- Squirrel updater, NOT always present
```

A second launch normally brings the existing window to the front. The single-instance lock uses the
user-data directory to identify that instance.

Choose a different directory to start a separate main process and profile. That instance also gets
its own renderers, GPU process, and crashpad handler.

```powershell
& "$env:LOCALAPPDATA\AnthropicClaude\app-<version>\claude.exe" --user-data-dir="$env:USERPROFILE\.claude-desktop-N"
```

Each directory stores its own sign-in, letting each instance use a different account.

Find the newest installed `app-*` directory each time. Do not hardcode a version or rely on the stub
launcher.

A manual or backup install does not create `%LOCALAPPDATA%\AnthropicClaude\claude.exe`.
Reinstalling can also remove an existing stub.

Use `-Directory` to exclude placeholder files left behind for blocked versions. These files share
the `app-<version>` naming scheme.

This machine has placeholder files `app-1.30096.1` and `app-1.30096.5`, sized 381 and 563 bytes.
Its only real install, `app-1.25927.0`, sorts below both.

### Verified on 2026-08-14

The check invoked one shortcut exactly as Windows does. The author then wrote this page from a
session inside that instance.

| Claim | Evidence |
|---|---|
| The stub forwarded `--user-data-dir` | The shortcut named the stub; the resulting process was `app-<version>\claude.exe` carrying the flag |
| The instance is separate, not a focused window | 10 processes carried the alternate profile path, beside a set carrying the default profile. The count moves with what the window has open |
| The launch is silent and visible | A window appeared, and no PowerShell console lingered |
| The default instance is unaffected | The pre-existing default-profile instance kept running throughout |
| The bundled Claude Code honors `CLAUDE_CONFIG_DIR` | `$env:CLAUDE_CONFIG_DIR` read `.claude-account-2`, with 4 session records under that root, from a session whose parent process is the desktop app |

On 2026-08-17, a reinstall removed `%LOCALAPPDATA%\AnthropicClaude\claude.exe` and `Update.exe`.
Every launcher naming the stub broke at once.

The first evidence row records earlier behavior; do not use it as launch instructions.

The last row verifies that bundled Claude Code reads `CLAUDE_CONFIG_DIR` from its parent process.
That observed behavior is the basis for using the variable here.

---

## The launcher, and the one line that is load-bearing

Create one shortcut per account to reopen its signed-in window.

Each account needs a launcher script and a shortcut:

1. A launcher script, at `%USERPROFILE%\claude-launchers\Launch-ClaudeDesktop-N.ps1`. Replace `N`
   with the account number in each copy.
2. A desktop shortcut targeting `powershell.exe` with
   `-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "<launcher path>"`.
3. That shortcut's Change Icon, pointed at `%LOCALAPPDATA%\AnthropicClaude\app-<version>\claude.exe`
   . Skip it and every shortcut shows the PowerShell icon, leaving N accounts indistinguishable on
   the desktop and in the taskbar.

```powershell
$ClaudeConfigDir = "$env:USERPROFILE\.claude-account-N"
$UserDataDir     = "$env:USERPROFILE\.claude-desktop-N"
$ClaudeRoot      = "$env:LOCALAPPDATA\AnthropicClaude"

$ClaudeExe = Get-ChildItem $ClaudeRoot -Filter 'app-*' -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match '^app-\d+(\.\d+){1,3}$' -and (Test-Path (Join-Path $_.FullName 'claude.exe')) } |
    Sort-Object { [version]$_.Name.Substring(4) } |
    Select-Object -Last 1 |
    ForEach-Object { Join-Path $_.FullName 'claude.exe' }
if (-not $ClaudeExe) { throw "No installed Claude Desktop under $ClaudeRoot (need app-<version>\claude.exe)." }

$env:CLAUDE_CONFIG_DIR = $ClaudeConfigDir
if (-not (Test-Path $ClaudeConfigDir)) {
    New-Item -ItemType Directory -Path $ClaudeConfigDir -Force | Out-Null
}

$claudeArgs = @("--user-data-dir=`"$UserDataDir`"") + ($args | ForEach-Object { "`"$_`"" })
Start-Process -FilePath $ClaudeExe -ArgumentList $claudeArgs -WindowStyle Normal
```

The first run opens an empty profile at a login screen. Sign in once; that shortcut will keep using
the account.

Keep `-WindowStyle Normal` on `Start-Process`. Without it, the app inherits the hidden PowerShell
window state and starts with no visible window.

Hidden PowerShell also hides launcher errors, including a missing install, unwritable config root,
or mistyped path. Run the `.ps1` in visible `pwsh` to see why a shortcut did nothing.

Only the icon path pins a version. Reset it by hand after an update removes that version; the
launcher finds the installed binary on each run.

If an instance misbehaves, remove all three `CLAUDE_CONFIG_DIR` pieces: the `$ClaudeConfigDir`
assignment, the `$env:` line, and the `Test-Path` /`New-Item` block. Any leftover reference may use
a missing variable.

`--user-data-dir` alone still gives the instance its own sign-in.

After that removal, Claude Code uses shared `~/.claude` credentials and session records.
`sessions.ps1` reports `desktop` for every affected instance, with no visible change in the app.

Appending `$args` lets files and folders dropped onto the shortcut reach the app. Quote each element
because `Start-Process -ArgumentList` joins with spaces without adding quotes.

Without those quotes, a dropped path containing a space arrives as two arguments.

### What each directory isolates

| Path | Isolates |
|---|---|
| `%USERPROFILE%\.claude-desktop-N` | The desktop app profile: sign-in, settings, cache, and that instance's `claude_desktop_config.json` |
| `%USERPROFILE%\.claude-account-N` | The Claude Code config root: credentials, settings, session records, transcripts |
| `%USERPROFILE%\.claude-account-N.lock` | Nothing. A lock artefact that is a DIRECTORY, not a config root. Never wire it: the name matches the `.claude-account-*` glob, and two installers here once did |
| `%USERPROFILE%\claude-launchers` | Nothing. It is where the scripts live |

### Check it on your own machine

Check the session account and the profile directory used by each open window.

Run both commands in the session you want to check:

```powershell
if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { "UNSET -- default ~/.claude" }
Get-CimInstance Win32_Process -Filter "Name='claude.exe'" | ForEach-Object {
    if ($_.CommandLine -match '--user-data-dir="([^"]+)"')  { $matches[1] }
    elseif ($_.CommandLine -match '--user-data-dir=([^"\s]+)') { $matches[1] }
} | Sort-Object -Unique
```

The first command prints a full path, such as `C:\Users\<you>\.claude-account-2`. `UNSET` means the
default instance uses `%USERPROFILE%\.claude`; its launcher does not set the variable.

The second command prints one path per open instance, including `%APPDATA%\Claude` for the default
profile. A raw `.CommandLine` dump includes extra processes and repeated paths.

Bundled Claude Code processes share the name but lack `--user-data-dir`. Each crashpad handler
repeats the profile path with extra flags.

---

## What the extra config roots cost the tooling here

The source machine has five roots: `.claude` and `.claude-account-1` through `.claude-account-4`.

Two installers accept one root per run: `install-coordination.ps1` uses `-SettingsPath`, and
`install-selfheal.ps1` uses `-ConfigDir`. Five roots require five runs of each.

`install-gate.ps1` covers every root in one run; see [INSTALL.md](INSTALL.md).

Install user-scope controls in every root a session can use. An unwired root can look governed from
inside a session; see [Running multiple sessions](RUNNING-MULTIPLE-SESSIONS.md).

The liveness fence scans every `~/.claude*` directory that holds a session registry. Presence,
occupancy, and overlap therefore see peers across accounts; see [Coordination](COORDINATION.md).

The login column in `scripts/worktree/sessions.ps1` identifies the account that owns each session.
See [Scripts](SCRIPTS.md).

`list_sessions` lists only sessions the app spawned, so announce reaches one account. This follows
from the [mechanism](LIMITS.md) and was not measured here.

Use [Session mail](SESSION-MAIL.md) for the cross-account case.

---

## Behaviour to expect

- The first launch of each shortcut opens a login screen. The profile starts empty. After signing
  in, the session persists in that profile.
- MCP servers are configured per profile. Each profile carries its own `claude_desktop_config.json`
  , so a new instance starts with no connectors. Copy the file from `%APPDATA%\Claude` to reuse the
  default profile's.
- The default profile is untouched. It still opens from the Start menu or the taskbar, as an
  additional instance beside the numbered ones.
- All instances group under one taskbar icon, because they are one executable.
- Deep links land wherever they land. The protocol handler and the native-messaging bridge resolve
  to whichever instance registered them. A `claude://` link will not reliably reach the instance you
  meant.
- Each instance is a full Electron app. Memory cost scales with the number of them.

### Limit: This is not a trust boundary

Separate Windows user accounts give each identity its own credential store and registry hive. They
also require fast user switching and duplicate environments.

This setup uses `--user-data-dir` to support several accounts under one login. Choose separate
Windows accounts if you need a security boundary.

---

## The icon check that reported a false match

While the stub existed, its icon was extracted and hashed alongside the real application icon. The
comparison checked whether the stub used a placeholder.

The first comparison hashed a `MemoryStream` without rewinding it. Every input therefore hashed as
zero bytes, falsely reporting identical icons.

An unrelated system executable produced the same hash, exposing the broken check. After rewinding
the streams, the controls differed and the stub matched the versioned binary exactly.

Test a comparison with inputs known to differ before trusting an equal result. The
[drift audit](CASE-STUDY-drift-audit.md) applies the same method to more controls.

---

## Related

| For | Read |
|---|---|
| Which surface to run several sessions on, and the channels between them | [Running multiple sessions](RUNNING-MULTIPLE-SESSIONS.md) |
| Finding a session across every login, and putting a relocated one back | [Scripts](SCRIPTS.md), [Worktrees](WORKTREES.md) |
| Reaching a peer under another account, which announce cannot | [Session mail](SESSION-MAIL.md) |
| Presence, occupancy and overlap, which read every config root | [Coordination](COORDINATION.md) |
| Wiring each config root, and proving the wiring is live | [INSTALL.md](INSTALL.md) |
| Every control's event and its fail-open or fail-closed posture | [Hooks](HOOKS.md) |
| Knowing when a pool is spent, which is per account | [Usage awareness](USAGE-AWARENESS.md) |
