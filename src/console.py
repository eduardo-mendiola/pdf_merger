"""
Console output formatting with colors and styles.
Provides a clean, professional terminal interface.
"""

# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Foreground colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Background colors
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


def print_header(title: str) -> None:
    """Print a styled header."""
    width = 60
    print()
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * width}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{title.center(width)}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * width}{Colors.RESET}")
    print()


def print_section(title: str) -> None:
    """Print a section header."""
    print()
    print(f"{Colors.BLUE}{Colors.BOLD}--- {title} ---{Colors.RESET}")
    print()


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}✓{Colors.RESET} {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"{Colors.RED}✗{Colors.RESET} {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"{Colors.CYAN}ℹ{Colors.RESET} {message}")


def print_prompt(message: str) -> None:
    """Print a prompt for user input."""
    print(f"{Colors.BOLD}{message}{Colors.RESET}", end=" ")


def print_summary(data: dict) -> None:
    """Print a formatted summary."""
    print()
    print(f"{Colors.BOLD}Summary:{Colors.RESET}")
    print(f"{Colors.DIM}{'-' * 40}{Colors.RESET}")
    for key, value in data.items():
        print(f"  {Colors.CYAN}{key}:{Colors.RESET} {value}")
    print(f"{Colors.DIM}{'-' * 40}{Colors.RESET}")
    print()


def print_file_added(filename: str) -> None:
    """Print a file added confirmation."""
    print(f"  {Colors.GREEN}+{Colors.RESET} {filename}")


def print_progress(message: str) -> None:
    """Print a progress message."""
    print(f"{Colors.MAGENTA}→{Colors.RESET} {message}")
