# АНАЛИЗ ДАННЫХ И ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ [in GameDev]
Отчет по лабораторной работе #4 выполнил(а):
- Чугунов Тимофей Анатольевич
- РИ-230932
Отметка о выполнении заданий (заполняется студентом):

| Задание | Выполнение | Баллы |
| ------ | ------ | ------ |
| Задание 1 | * | 20 |
| Задание 2 | * | 60 |
| Задание 3 | * | 60 |

знак "*" - задание выполнено; знак "#" - задание не выполнено;

Работу проверили:
- к.т.н., доцент Денисов Д.В.
- к.э.н., доцент Панов М.А.
- ст. преп., Фадеев В.О.

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Структура отчета

- Данные о работе: название работы, фио, группа, выполненные задания.
- Цель работы.
- Задание 1.
- Код реализации выполнения задания. Визуализация результатов выполнения (если применимо).
- Задание 2.
- Код реализации выполнения задания. Визуализация результатов выполнения (если применимо).
- Задание 3.
- Код реализации выполнения задания. Визуализация результатов выполнения (если применимо).
- Выводы.
- ✨Magic ✨

## Цель работы
Ознакомиться с моделью перцептрона, испытать его в различных методах, построить наглядную модель.


## Задание 1: в проекте Unity реализовать перцептрон, который умеет производить вычисления:
## OR | дать комментарии о корректности работы
В проекте Unity релизован перциптрон с функцией вычисления OR, входные и выходные данные указаны на скриншоте. В результате выбранной Epoch amount = 8, мы получаем TotalError = 0. Следовательно, перцептрон работает корректно.

Как реализована функция OR: 
![image](https://github.com/user-attachments/assets/4171ceca-0b6b-4057-97c5-6fbdc6f12871)

Скриншота функций на модели в Unity:
![image](https://github.com/user-attachments/assets/86eb9606-dad1-4fa4-8505-eab4ffcb44ee)


## AND | дать комментарии о корректности работы
В проекте Unity релизован перциптрон с функцией вычисления AND, входные и выходные данные указаны на скриншоте. В результате выбранной Epoch amount = 10, мы получаем TotalError = 0. Следовательно, перцептрон работает корректно.

Как реализована функция AND: 
![image](https://github.com/user-attachments/assets/523f39d3-c55f-4887-b902-4a3e6a45e461)


Скриншота функций на модели в Unity:
![image](https://github.com/user-attachments/assets/c57596a5-164d-49cc-a0ea-ec34ed2362b3)



## NAND | дать комментарии о корректности работы
В проекте Unity релизован перциптрон с функцией вычисления NAND, входные и выходные данные указаны на скриншоте. В результате выбранной Epoch amount = 12, мы получаем TotalError = 0. Следовательно, перцептрон работает корректно.

Как реализована функция NAND (Является инверсией для AND): 
![image](https://github.com/user-attachments/assets/591aea0c-ba03-405a-9f96-8da34cba8b22)



Скриншота функций на модели в Unity:
![image](https://github.com/user-attachments/assets/e11194e6-bf08-42b5-a2c2-e4f4f489d754)



## XOR | дать комментарии о корректности работы
В проекте Unity релизован перциптрон с функцией вычисления XOR, входные и выходные данные указаны на скриншоте. В результате выбранной Epoch amount = 16, мы получаем TotalError = 0. Следовательно, перцептрон работает корректно. XOR не является линейно разделимой функцией, поэтому простой перцептрон (один слой) не сможет обучиться корректно. Для работы этой функции и для дальнейшей привязки ко 2 заданию, был создан отдельный код:

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.IO;

public class XOR_Perceptron : MonoBehaviour
{
    [System.Serializable]
    public class TrainingSet
    {
        public double[] input;
        public double output;
    }
    [SerializeField] private string name;
    [SerializeField] private int epochAmount;
        
        
    [SerializeField] private GameObject box1;
    [SerializeField] private GameObject box2;
	
    [SerializeField] private GameObject resultBox;
	
    private Color boxValue;
        
    public TrainingSet[] ts;

    private double[,] weightsInputHidden;
    private double[] weightsHiddenOutput;
    private double[] hiddenLayer;
    private double[] biasesHidden;
    private double biasOutput;
    private double learningRate = 0.1;
    private StreamWriter writer = new StreamWriter("output.csv");

    private string sheetId = "1s1AhpZU16Qcbkl71SKyP50BRlhhSsHSCXNyD2cTfrpg"; // Замените на ID вашей таблицы
    private string apiKey = "AIzaSyAfYRYdMIrptX7YaABRg2gmC_G6a78oE5I"; // Замените на ваш ключ API
    public string sheetName = "LoLone"; // Название листа в таблице

    void InitialiseWeights()
    {
        weightsInputHidden = new double[2, 2];
        weightsHiddenOutput = new double[2];
        biasesHidden = new double[2];

        for (int i = 0; i < 2; i++)
        {
            for (int j = 0; j < 2; j++)
            {
                weightsInputHidden[i, j] = Random.Range(-1.0f, 1.0f);
            }
            weightsHiddenOutput[i] = Random.Range(-1.0f, 1.0f);
            biasesHidden[i] = Random.Range(-1.0f, 1.0f);
        }

        biasOutput = Random.Range(-1.0f, 1.0f);
        hiddenLayer = new double[2];
    }

    double Sigmoid(double x)
    {
        return 1.0 / (1.0 + Mathf.Exp((float)-x));
    }

    double SigmoidDerivative(double x)
    {
        return x * (1 - x);
    }

    void Train(int epochs)
    {
        InitialiseWeights();

        for (int epoch = 1; epoch <= epochs; epoch++)
        {
            double totalError = 0;

            foreach (var data in ts)
            {
                // Forward pass
                for (int i = 0; i < 2; i++)
                {
                    hiddenLayer[i] = 0;
                    for (int j = 0; j < 2; j++)
                    {
                        hiddenLayer[i] += data.input[j] * weightsInputHidden[j, i];
                    }
                    hiddenLayer[i] += biasesHidden[i];
                    hiddenLayer[i] = Sigmoid(hiddenLayer[i]);
                }

                double output = 0;
                for (int i = 0; i < 2; i++)
                {
                    output += hiddenLayer[i] * weightsHiddenOutput[i];
                }
                output += biasOutput;
                output = Sigmoid(output);

                // Backpropagation
                double outputError = data.output - output;
                double outputGradient = outputError * SigmoidDerivative(output);

                for (int i = 0; i < 2; i++)
                {
                    double hiddenError = outputGradient * weightsHiddenOutput[i];
                    double hiddenGradient = hiddenError * SigmoidDerivative(hiddenLayer[i]);

                    for (int j = 0; j < 2; j++)
                    {
                        weightsInputHidden[j, i] += learningRate * hiddenGradient * data.input[j];
                    }

                    biasesHidden[i] += learningRate * hiddenGradient;
                    weightsHiddenOutput[i] += learningRate * outputGradient * hiddenLayer[i];
                }

                biasOutput += learningRate * outputGradient;

                totalError += Mathf.Abs((float)outputError);
            }

            // Запись ошибки
            //Debug.Log((epoch, totalError));
            
            //writer.WriteLine($"{epoch},{totalError}");
            //UploadEpochAndError(epoch, totalError);
        }
    }

    double CalcOutput(double[] input)
    {
        for (int i = 0; i < 2; i++)
        {
            Debug.Log((input[0], input[1]));
            hiddenLayer[i] = 0;
            for (int j = 0; j < 2; j++)
            {
                hiddenLayer[i] += input[j] * weightsInputHidden[j, i];
            }
            hiddenLayer[i] += biasesHidden[i];
            hiddenLayer[i] = Sigmoid(hiddenLayer[i]);
        }

        double output = 0;
        for (int i = 0; i < 2; i++)
        {
            output += hiddenLayer[i] * weightsHiddenOutput[i];
        }
        output += biasOutput;
        return Sigmoid(output) > 0.5 ? 1 : 0;
    }



    void Start()
    {
        Train(epochAmount);
        float box1Value = Mathf.Round(box1.GetComponent<Renderer>().material.color.r);
        float box2Value = Mathf.Round(box2.GetComponent<Renderer>().material.color.r);
        
        Debug.Log((box1Value, box2Value));
        double[] data = { box1Value, box2Value };
        float resultColor = (float)CalcOutput(data);
        Debug.Log(resultColor);
        
        boxValue = new Color(resultColor, resultColor, resultColor);
        resultBox.GetComponent<Renderer>().material.color = boxValue;
    }

    [System.Serializable]
    private class ValueRange
    {
        public string[][] values;
    }
}


Как реализована функция XOR: 
![image](https://github.com/user-attachments/assets/019e248f-5711-4188-8169-2123e2e2382f)




Скриншота функций на модели в Unity:
![image](https://github.com/user-attachments/assets/c69a13ec-0657-4412-84d7-57c5c94c8908)



## Задание 2: Построить графики зависимости количества эпох от ошибки  обучения. Указать от чего зависит необходимое количество эпох обучения.

В простых задачах, таких как AND, OR, NAND, количество эпох можно держать небольшим (5-10 эпох). В сложных задачах (XOR), однослойный перцептрон не решит задачу даже при большом количестве эпох — для её решения нужен многослойный перцептрон.
В начале обучения ошибка высокая, так как веса инициализированы случайным образом и выходы перцептрона далеко от ожидаемых значений.
По мере увеличения количества эпох обучения (количество проходов по всем данным) веса корректируются, ошибка уменьшается.
Для простых задач, таких как AND, OR и NAND (линейно разделимые функции), ошибка может полностью уменьшиться до 0 за небольшое количество эпох.
Однако для более сложных задач (например, XOR) уменьшение ошибки невозможно для однослойного перцептрона, поскольку данные нелинейно разделимы.

Графики находятся в Google sheets, реализованные с помощью API (которым научились пользоваться в предыдущих ЛР). Все данные в графики подгружаются автоматически при запуске программы XOR_Perceptron.
Ссылка: https://docs.google.com/spreadsheets/d/1CiSGvzlOJaCgRrBx1xx-dgZlKz_Tnl14bQtB9BWukwM/edit?gid=1451694720#gid=1451694720


## Задание 3: Построить визуальную модель работы перцептрона на сцене Unity.
Самое простое задание на мой взгляд, готовые функции и зависимости просто перекидываем на объекты, я выбрал кубы. Полная сборка (Unity + коды) прикрпил в гугл форму. Удивительное наблюдение: при каждом запуске проекта, кубы меняют свой цвет
![image](https://github.com/user-attachments/assets/9f4b17cb-c408-4b07-a0b2-c91cb401ae76)
![image](https://github.com/user-attachments/assets/e540b1f4-172e-4161-923c-8dd9f189e422)


## Выводы

Абзац умных слов о том, что было сделано и что было узнано:
В этой работе я узнал о простом ИИ, которое можно использовать в играх и не только, научился с ним взаимодейстовать и обучать. Одна из самых интересных, но и в то же время сложных работ.

| Plugin | README |
| ------ | ------ |
| Dropbox | [plugins/dropbox/README.md][PlDb] |
| GitHub | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |
| OneDrive | [plugins/onedrive/README.md][PlOd] |
| Medium | [plugins/medium/README.md][PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md][PlGa] |

## Powered by

**BigDigital Team: Denisov | Fadeev | Panov**
