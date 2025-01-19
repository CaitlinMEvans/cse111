"""
This program demonstrates that numbers are passed to a function by value,
and lists are passed to a function by reference.
"""

def main():
    """The main function initializes variables and demonstrates
    how passing numbers and lists to a function behaves differently.
    """
    print("main()")

    # Initialize an integer and a list
    x = 5
    lx = [7, -2]
    print(f"    Before calling modify_args(): x {x}  lx {lx}")

    # Pass the integer and list to the modify_args function
    modify_args(x, lx)

    # Display values after modify_args runs
    print(f"    After calling modify_args():  x {x}  lx {lx}")


def modify_args(n, alist):
    """This function demonstrates how integers and lists behave differently
    when passed as arguments to a function.

    Parameters:
        n: A number (integer) passed by value.
        alist: A list passed by reference.
    """
    print("    modify_args(n, alist)")
    print(f"        Before changing n and alist: n {n}  alist {alist}")

    # Modify both the number and the list
    n += 1  # This won't affect the original integer 'x' in main
    alist.append(4)  # This will affect the original list 'lx' in main

    print(f"        After changing n and alist:  n {n}  alist {alist}")


# This ensures the main function is only executed
# when the file is run directly, not when imported
if __name__ == "__main__":
    main()