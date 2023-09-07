from argparser import get_args
from scraping import scrape_models

if __name__ == "__main__":

    args = get_args()

    print(args)
    dict = scrape_models(args.version, args.architecture)

    output_list = []

    print('Checking {} Models'.format(len(dict)))
    for key, value in dict.items():
        breaking = False
        for impl_class in value:
            for wanted_class in args.classes:
                if wanted_class in impl_class:
                    output_list.append(value[0])
                    breaking = True
                    break
            if breaking:
                break

    print('A total of {} implement at least one of the specified classes.'.format(len(output_list)))
    with open('tmp/models.txt', 'w') as f:
        f.write(str(output_list))
