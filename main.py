import Flask
import Calculator

labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]

Calculator.create_pie_chart(labels, sizes)