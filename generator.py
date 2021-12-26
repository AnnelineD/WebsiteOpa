import os
from glob import glob
from jinja2 import Environment, FileSystemLoader


class Generator:
    def __init__(self, poems_dir="poems", templates_dir="templates", out_dir="docs"):
        self.poems = [os.path.basename(path).replace('.txt', '') for path in glob(f"{poems_dir}/*.txt")]
        self.titles = []
        self.poems_dir = poems_dir
        self.out_dir = out_dir
        print(self.poems)
        self.env = Environment(loader=FileSystemLoader([out_dir, templates_dir]),
                               autoescape=False, trim_blocks=True, lstrip_blocks=True)

    def generate(self, out_dir='docs'):
        base = self.env.get_template("base.html")
        with open(f"{out_dir}/index.html", 'w') as f:
            f.write(base.render(poems=[[f"{poem}.html", poem] for poem in self.poems],
                                titles=[[self.titles[i], self.poems[i]] for i in range(len(self.titles))]))

    @staticmethod
    def txt_to_html(in_path, out_path):
        assert(os.path.isfile(in_path))
        title = ""
        with open(in_path) as in_f, open(out_path, "w") as out_f:
            title = in_f.readline()
            out_f.write(f"<h1>{title}</h1>\n")
            first = in_f.readline()
            if first != '\n':
                out_f.write(f"{first}\n")
            out_f.write(f'<pre class="poem-text">{in_f.read()}</pre>')
        return title

    def convert_all_poems(self):
        for poem in self.poems:
            self.titles.append(self.txt_to_html(os.path.join(self.poems_dir, f"{poem}.txt"),
                                                os.path.join(self.out_dir, f"{poem}.html")))


if __name__ == '__main__':
    g = Generator()
    g.convert_all_poems()
    g.generate()


