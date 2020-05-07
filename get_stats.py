import numpy
import matplotlib.pyplot as plt
locations = ["Cincinnati", "UKansasState", "Atlanta", "Philadelphia", "Boston", "Berlin",\
			 "Champaign", "NYC", "Denver", "SanFrancisco", "UMissouri", "Toronto", "Roanoke"]
optimal_solutions = [277952, 62962, 2003763, 1395981, 893536, 7542,\
					 52643, 1555060, 100431, 810196, 132709, 1176151, 655454]
method = 'LS2'

data = {}
for i in range(len(locations)):
    loc = locations[i]
    data[loc] = {}
    for seed in range(1,11):
        t = []
        q = []
        f = open('output/%s/%s_%s_5_%d.trace' % (method.lower(), loc, method, seed))
        for line in f:
            t.append(float(line.split(',')[0]))
            q.append(int(line.split(',')[1]))
        f.close()
        data[loc][seed] = {
            'time': t,
            'quality': q
        }

print('Dataset&Time(s)&Sol.Q&Rel.Err\\\\ \\hline')
for i in range(len(locations)):
    loc = locations[i]
    t = []
    q = []
    for seed in range(1,11):
        t.append(data[loc][seed]['time'][-1])
        q.append(data[loc][seed]['quality'][-1])
    t = numpy.mean(t)
    q = numpy.mean(q)
    relErr = 1.0 * (q - optimal_solutions[i]) / optimal_solutions[i]
    print('%s&%.2f&%.0f&%.4f\\\\ \\hline'%(loc,t,q,relErr))

#draw box plots for Toronto and Roanoke/UMissouri
times = []
labels = []
for i in range(len(locations)-3, len(locations)-1):
    loc = locations[i]
    O = optimal_solutions[i]
    t5 = []
    t10 = []
    for seed in range(1,11):
        for j in range(len(data[loc][seed]['time'])):
            t = data[loc][seed]['time'][j]
            q = data[loc][seed]['quality'][j]
            relErr = 1.0 * (q - optimal_solutions[i]) / optimal_solutions[i]
            if relErr < 0.05 and len(t5)<seed:
                t5.append(t)
            if relErr < 0.1 and len(t10)<seed:
                t10.append(t)
        f.close()
    times.append(t5)
    times.append(t10)
    labels.append('%s 5%%'%loc)
    labels.append('%s 10%%'%loc)

plt.figure()
plt.boxplot(times, labels=labels)
plt.ylabel('Running time (s)')
plt.title('Boxplot for %s'%method)
plt.savefig('plots/boxplot_%s.png'%method)

#draw QRTD for Toronto and Roanoke/UMissouri
for i in range(len(locations)-3, len(locations)-1):
    loc = locations[i]
    O = optimal_solutions[i]
    times = []
    probabilities = []
    max_time = 0
    margins = [0.3,0.35,0.4,0.45,0.5]
    for margin in margins:
        threshold = O * (1+margin)
        t = []
        for seed in range(1,11):
            q = numpy.array(data[loc][seed]['quality'])
            reached = q < threshold
            if numpy.any(reached):
                first_idx = numpy.nonzero(reached)[0][0]
                t.append(data[loc][seed]['time'][first_idx])
        t = sorted(t)
        max_time = max(max_time, max(t))
        p = (1+numpy.arange(len(t)))*0.1
        times.append(t)
        probabilities.append(list(p))
    plt.figure()
    for j in range(len(times)):
        times[j].append(max_time)
        probabilities[j].append(probabilities[j][-1])
        plt.plot(times[j], probabilities[j], label='%.1f%%' % (margins[j]*100))
    plt.xlabel('Running time (s)')
    plt.ylabel('P(solve)')
    plt.legend()
    plt.title('Qualified Run Time Distribution for %s' % loc)
    plt.savefig('plots/qrtd_%s_%s.png'%(loc,method))

#draw SQD for Toronto and Roanoke/UMissouri
for i in range(len(locations)-3, len(locations)-1):
    loc = locations[i]
    O = optimal_solutions[i]
    qualities = []
    probabilities = []
    max_quality = 0
    times = [1, 1.5, 2, 2.5, 5]
    for threshold in times:
        q = []
        for seed in range(1, 11):
            t = numpy.array(data[loc][seed]['time'])
            reached = t <= threshold
            if numpy.any(reached):
                last_idx = numpy.nonzero(reached)[0][-1]
                x = data[loc][seed]['quality'][last_idx]
                relErr = 100.0 * (x - O) / O
                q.append(relErr)
        q = sorted(q)
        max_quality = max(max_quality, max(q))
        p = (1+numpy.arange(len(q)))*0.1
        qualities.append(q)
        probabilities.append(list(p))
    plt.figure()
    for j in range(len(times)):
        qualities[j].append(max_quality)
        probabilities[j].append(probabilities[j][-1])
        plt.semilogx(qualities[j], probabilities[j], label='%.2fs' % (times[j]))
    plt.xlabel('Relative solution quality (%)')
    plt.ylabel('P(solve)')
    plt.legend()
    plt.title('Solution Quality Distribution for %s' % loc)
    plt.savefig('plots/sqd_%s_%s.png'%(loc,method))
