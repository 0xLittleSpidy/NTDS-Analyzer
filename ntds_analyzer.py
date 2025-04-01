import argparse
import time
import threading
import asyncio
import sys
import shutil

def parse_ntds_file(file_path):
    users_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) > 3:
                username = parts[0]
                nthash = parts[3]
                if nthash:
                    users_data[username] = nthash
    return users_data

def analyze_password_reuse(users_data):
    total_users = len(users_data)
    reused_passwords = {}
    for user, password in users_data.items():
        if password in reused_passwords:
            reused_passwords[password].append(user)
        else:
            reused_passwords[password] = [user]

    reused_password_count = sum(1 for users in reused_passwords.values() if len(users) > 1)
    users_with_reused_passwords = sum(len(users) for users in reused_passwords.values() if len(users) > 1)
    unique_reused_passwords = len([password for password, users in reused_passwords.items() if len(users) > 1])
    worst_case_blast_radius = max(len(users) for users in reused_passwords.values())
    average_blast_radius = sum(len(users) - 1 for users in reused_passwords.values()) / total_users

    result = []
    result.append("-- Password Reuse Summary --")
    result.append("(Note: Analysis excludes disabled users and users with empty passwords)")
    result.append(f"# Users with the exact SAME or SIMILAR password as another user: {users_with_reused_passwords} out of {total_users}")
    result.append(f"% Users with the exact SAME or SIMILAR password as another user: {users_with_reused_passwords / total_users * 100:.3f}")
    result.append(f"{unique_reused_passwords} password(s) are being used by these {users_with_reused_passwords} users")
    result.append("")
    result.append("-- Blast Radius: # Additional Accounts That Can Be Compromised if a Single Account is Compromised --")
    result.append(f"Worst case password reuse blast radius: {worst_case_blast_radius}")
    result.append(f"Average password reuse blast radius (equal to 0 when everyone has a unique, dissimilar password): {average_blast_radius:.3f}")
    result.append("")
    result.append("-- List of Users and Their Shared Passwords --")
    for password, users in reused_passwords.items():
        if len(users) > 1:
            result.append(f"Password Hash: {password} is used by users: {', '.join(users)}")
    return result

async def main(args):
    start_time = time.time()
    users_data = parse_ntds_file(args.file)
    result = analyze_password_reuse(users_data)
    
    if args.debug:
        for line in result:
            print(line)
    else:
        columns = shutil.get_terminal_size().columns
        for i in range(101):
            time.sleep(0.05)
            sys.stdout.write(f"\r[{'#' * (i // 2)}{' ' * (50 - i // 2)}] {i}%")
            sys.stdout.flush()
        sys.stdout.write("\n")
        for line in result:
            print(line)
    
    if args.output:
        with open(args.output, 'w') as file:
            for line in result:
                file.write(line + '\n')
    
    end_time = time.time()
    print(f"\nTime taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze NTDS.DIT Database for password reuse\nThis tool is developed by 0xLittleSpidy")
    parser.add_argument('-f', '--file', required=True, help="File containing NTDS.DIT Database")
    parser.add_argument('-de', '--debug', action='store_true', help="Enable debug mode to show detailed logs")
    parser.add_argument('-o', '--output', help="Output file to store results")
    parser.add_argument('-h', '--help', action='help', help="Show this help message and exit")
    
    args = parser.parse_args()
    asyncio.run(main(args))
