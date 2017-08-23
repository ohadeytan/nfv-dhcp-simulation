import graphviz as gv
import imageio
from time import sleep

colors = { 'DHCP_DISCOVER' : 'blue',
           'DHCP_OFFER'    : 'red',
           'DHCP_REQUEST'  : 'yellow',
           'DHCP_ACK' : 'green'
         }



def getRecords(file_name, limit=float('Inf'), verbose=False):
    records = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if line[0] == '-':
                continue
            line = line.split(':')
            ip, ty, home = eval(line[-1].strip()), line[1][:-4].strip(), int(line[2][:-2].strip())
            if home > limit:
                continue
            records.append((ty, home, ip))
            if verbose:
                print(records[-1])
    return records
          
def main():
    records = getRecords("output_example.txt", 10)
    homes = set(str(r[1]) for r in records)

    g = gv.Graph(format='png', )
    g.node('Server', style='filled', color='gold')
    g.body.extend(['layout=circo', ])
    for i in homes:
        g.node(i, label=i, fontsize='20', style='filled', color='blueviolet', shape='Square')
        g.edge('Server', str(i),  )
        devices = set(str(r[2]) for r in records if str(r[1]) == i and r[0] == 'DHCP_OFFER')
        for j in devices:
            g.node(j, label='', style='filled')
            g.edge(i, j)

    counter = 0
    g.render('{:03d}'.format(counter))
    images = []
    for record in records:
        if not record[0] == 'DHCP_DISCOVER':
            g.node(str(record[2]), color=colors[record[0]])
            counter += 1
            g.render('{:03d}'.format(counter))
            images.append(imageio.imread('{:03d}.png'.format(counter)))
    imageio.mimsave('animation.gif', images)

    


if __name__ == '__main__':
    main()
