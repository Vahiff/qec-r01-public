# QEC-R01 — Gemini Review Report

**Record status:** FULL OWNER-SUPPLIED TRANSCRIPT / ORIGINAL VERBATIM FIDELITY NOT INDEPENDENTLY VERIFIED.

**Received from owner:** 26 October 2026. The text below was supplied by the repository owner and partially visually corroborated by retained screenshots of a Gemini Pro conversation. Its complete character-for-character correspondence with the original AI response, model metadata and full chronology have not been independently authenticated. It is not journal peer review, not an institutional Google evaluation and not a review by a named Google employee.

**Reported recommendation:** Reject.

## Full owner-supplied review text

Review Report

1. Summary

Авторы представляют так называемое исследование квантовой коррекции ошибок, анализируя работу максимального апостериорного (MAP) декодера для 3-кубитного кода повторения при наличии независимого шума Pauli-X и коррелированных двухкубитных X-ошибок. Модель оценивается путем точного перебора всего восьми классических масок ошибок. В работе нет ни физического эксперимента, ни симуляции физического уровня, а есть лишь тривиальная однораундовая симуляция пропускной способности кода (code-capacity). Это классическая студенческая задача по теории вероятностей, маскирующаяся под статью для ведущего физического журнала.

2. Major Concerns

 * Фундаментальная бессмысленность 3-кубитной игрушечной модели: Авторы исследуют код, который корректирует только изолированные ошибки X, в то время как полная квантовая дистанция этого кода равна 1, поскольку Z-ошибки вообще не исправляются. Это тривиальный классический код повторения, и сами авторы вынуждены признать, что коррекция произвольных одиночных ошибок Паули на трех кубитах невозможна из-за нарушения квантовой границы Синглтона. Статья не имеет никакого отношения к реальной квантовой отказоустойчивости.
 * Полное отсутствие реального "железа": В статье прямо заявлено, что это не демонстрация на квантовом устройстве. Модель предполагает идеальное считывание синдрома и полностью игнорирует ошибки вентилей, ошибки измерений, утечки, аппаратный дрейф и Y/Z шум. Публикация чисто программного скрипта идеализированных битовых переворотов без единого запуска на реальном квантовом процессоре неприемлема.
 * Нелепое оправдание с QuTiP: Авторы заявляют, что написали симуляцию матрицы плотности в QuTiP с затуханием амплитуды, но не смогли ее запустить, потому что установка пакета завершилась ошибкой из-за проблем с разрешением DNS-имен. Включение в академическую статью жалоб на то, что у авторов пропал интернет при скачивании библиотеки — это откровенное издевательство над процессом рецензирования и здравым смыслом.
 * Смехотворный размер выборки: Авторы гордятся генерацией 2000 калибровочных репликаций с использованием псевдослучайного генератора на Python. В эпоху современной вычислительной физики выборка в 2000 итераций для игрушечной биномиальной модели вызывает лишь недоумение. Применять доверительные интервалы Уилсона к крошечной программной симуляции, выдавая это за строгий анализ — абсурд.
 * Незавершенное исследование ("NOT RUN"): Половина заявленной работы попросту не выполнена. Авторы открыто пишут, что другие точки сетки параметров шума и независимая оценка Монте-Карло остались в статусе "NOT RUN". Статья отправлена в журнал до того, как код успел отработать свои циклы.

3. Verdict

Reject.

## Evidence and caveats

The report's wording is preserved as supplied by the owner, including allegations about journal submission. The repository does not independently substantiate those allegations. Screenshots exposing email accounts were removed from the current working tree. Deleted Git files may remain accessible in earlier Git history until a separately authorized history-remediation process is carried out.
