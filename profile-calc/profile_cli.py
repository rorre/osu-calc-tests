import sys, requests, profile_calc
import click

def brk():
    click.echo("----------------")

@click.command()
@click.option('--key', default="", help="osu! API key.")
@click.option('--user', default="", help="User to be calculated.")
@click.option("--limit", default=100, help="Limit top n score (Default: 100 | Max: 100)")
def main(key, user, limit):
    if not key:
        click.echo("Please input osu! API key!")
        return
    if not user:
        click.echo("Please specify a user!")
        return
    url = 'https://osu.ppy.sh/api/get_user?k={}&u={}'.format(key, user)
    js = requests.get(url).json()
    if type(js) == dict and "error" in js.keys():
        click.echo("Invalid API key. Make sure that you have typed your API key correctly.")
    if not js:
        click.echo("Invalid username. Check to see if you made a typo or maybe the user is restricted.")
    profile_pp = float(js[0]['pp_raw'])
    pp_info = profile_calc.return_values(user, key)
    old_sorted_list = [i for i in
                       sorted(pp_info, key=lambda x: x[2], reverse=True)]
    old_pp = sum([old_sorted_list[i][2] * (0.95 ** i) for i in range(len(old_sorted_list))])
    new_sorted_list = [i for i in
                       sorted(pp_info, key=lambda x: x[1], reverse=True)]
    new_pp = sum([new_sorted_list[i][1] * (0.95 ** i) for i in range(len(new_sorted_list))])
    sorted_list = new_sorted_list
    brk()
    with open("result.txt", "w") as f:
        for i in sorted_list:
            f.write(i[0])
            f.write("Old: {:.2f}pp\n".format(i[2]))
            f.write("New: {:.2f}pp\n".format(i[1]))
            f.write("Percentage: {:.2g}%\n".format(100 * i[2] / i[1]))
            f.write("\n")
            click.echo(i[0])
            click.echo("Old: {:.2f}pp".format(i[2]))
            click.echo("New: {:.2f}pp".format(i[1]))
            click.echo("Percentage: {:.2g}%".format(100 * i[2] / i[1]))
            brk()
        f.write("old pp: {:.2f}\n".format(profile_pp))
        f.write("new pp: {:.2f}\n".format(new_pp + (profile_pp - old_pp)))
    click.echo("old pp: {:.2f}".format(profile_pp))
    click.echo("new pp: {:.2f}".format(new_pp + (profile_pp - old_pp)))
    click.echo("Result logged in 'result.txt' file.")

if __name__ == "__main__":
    main()