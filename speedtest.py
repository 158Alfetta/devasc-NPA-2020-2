import statistics
import csv
def main():
    sheet = csv.reader(open("speedtest_27.csv"))
    #Server ID,Sponsor,Server Name,Timestamp,Distance,Ping,Download,Upload,Share,IP Address
    latency = []
    down = []
    up = []
    for row in sheet:
        latency.append(float(row[-5]))
        down.append(float(row[-4])/1000000)
        up.append(float(row[-3])/1000000)
        server_id = row[0]
        sponser = row[1]
    print("----------------------")
    print("Server ID: ", server_id)
    print("Server Name: ", sponser)
    print("Download Max: %.2f Mbps | Min: %.2f Mbps | Avg: %.2f Mbps | SD %.2f Mbps" %(max(down), min(down), sum(down)/len(down), statistics.stdev(down)))
    print("Upload Max: %.2f Mbps | Min: %.2f Mbps | Avg: %.2f Mbps | SD %.2f Mbps" %(max(up), min(up), sum(up)/len(up), statistics.stdev(up)))
    print("Latency Max: %.2f ms | Min: %.2f ms | Avg: %.2f ms | SD %.2f ms" %(max(latency), min(latency), sum(latency)/len(latency), statistics.stdev(latency)))
    print("----------------------")
main()