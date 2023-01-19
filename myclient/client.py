import requests
import math

def help():
    print('register: Prompts user for a username, password, and email to create a new account\n')
    print('login (url): Prompts user for their username and password to login to their account\n')
    print('\turl should be sc21atw.pythonanywhere.com\n')
    print('The following commands all require the user to be signed in to use\n')
    print('logout: Logs out the current user (if logged in)\n')
    print('list: Prints a list of all module instances and the professors that are teaching them\n')
    print('view: Prints a list of all professors and their overall ratings\n')
    print('average (professor_id) (module_code): Prints the average rating for the professor in the module specified\n')
    print('rate (professor_id) (module_code) (year) (semester) (rating): Gives the specified module professor a given rating\n')

def custom_round(x):
    if isinstance(x, int):
        return x
    ceiling = math.ceil(x)
    if ceiling - x > .5:
        return math.floor(x)
    elif ceiling - x <= .5:
        return ceiling

if __name__ == '__main__':
    s = requests.session()
    while True:
        comm = input('Enter a valid command (type help for all commands or exit to exit the program): ')
        split_comm = comm.split(" ")
        if len(split_comm) == 1:
            if comm == 'help':
                help()


            elif comm == 'register':
                un = input('Enter a username: ')
                email = input('Enter an email: ')
                pw = input('Enter a password: ')
                post_data = {
                    'username': un,
                    'email': email,
                    'password': pw
                }
                response = s.post('https://sc21atw.pythonanywhere.com/register/', data = post_data)
                response_data = response.json()
                print(response_data['status'], ': ', response_data['result'], sep = '')


            elif comm == 'logout':
                response = s.post('https://sc21atw.pythonanywhere.com/logout/')
                response_data = response.json()
                print(response_data['status'], ': ', response_data['result'], sep = '')


            elif comm == 'list':
                response = s.get('https://sc21atw.pythonanywhere.com/list/')
                response_data = response.json()
                if response_data['status'] == 'Failed':
                    print(response_data['status'], ': ', response_data['result'], sep = '')
                else:
                    print('{:>5} {:>35} {:>5} {:>2}\tProfessors'.format('Code', 'Name', 'Year', 'Semester'))
                    print('-' * 150)
                    for entry in response_data['result']:
                        print('{:>5} {:>35} {:>5} {:>2}'.format(entry['code'], entry['name'], str(entry['year']), str(entry['sem'])), end = '\t')
                        rep_string = ''
                        for prof in entry['names']:
                            rep_string += entry['names'][prof] + ', ' + prof + '; '
                        print(rep_string)


            elif comm == 'view':
                response = s.get('https://sc21atw.pythonanywhere.com/view/')
                response_data = response.json()
                if response_data['status'] == 'Failed':
                    print(response_data['status'], ': ', response_data['result'], sep = '')
                else:
                    all_profs = response_data['result']
                    for prof in all_profs:
                        if prof['rating'] == 0:
                            final_string = 'There are no ratings for ' + prof['name'] + ' (' + prof['id'] + ')'
                            print(final_string)
                        else:
                            stars = '*' * custom_round(prof['rating'])
                            final_string = 'The rating of ' + prof['name'] + ' (' + prof['id'] + ') is ' + stars
                            print(final_string)


            elif comm == 'exit':
                break


            else:
                print('That is not a valid command. Type help to see all valid commands')
        else:
            if split_comm[0] == 'login' and len(split_comm) == 2:
                url = split_comm[1]
                un = input('Enter your username: ')
                pw = input('Enter your password: ')
                post_data = {
                    'username': un,
                    'password': pw
                }
                response = s.post('https://sc21atw.pythonanywhere.com/login/', data = post_data)
                response_data = response.json()
                print(response_data['status'], ': ', response_data['result'], sep = '')


            elif split_comm[0] == 'average' and len(split_comm) == 3:
                prof_id = split_comm[1]
                mod_code = split_comm[2]
                get_data = {
                    'professor_id': prof_id,
                    'module_code': mod_code
                }
                response = s.get('https://sc21atw.pythonanywhere.com/average/', params = get_data)
                response_data = response.json()
                if response_data['status'] == 'Failed':
                    print(response_data['status'], ': ', response_data['result'], sep = '')
                else:
                    stars = '*' * custom_round(response_data['result'])
                    print_string = 'The rating of ' + response_data['prof'] + ' (' + prof_id + ') in module ' + \
                        response_data['module'] + ' (' + mod_code + ') is ' + stars
                    print(print_string)


            elif split_comm[0] == 'rate' and len(split_comm) == 6:
                prof_id = split_comm[1]
                mod_code = split_comm[2]
                yr = int(split_comm[3])
                sem = int(split_comm[4])
                rate = int(split_comm[5])
                post_data = {
                    'professor_id': prof_id,
                    'module_code': mod_code,
                    'year': yr,
                    'semester': sem,
                    'rating': rate
                }
                response = s.post('https://sc21atw.pythonanywhere.com/rate/', data = post_data)
                response_data = response.json()
                print(response_data['status'], ': ', response_data['result'], sep = '')


            else:
                print('That is not a valid command. Type help to see all valid commands')