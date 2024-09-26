#内置库
import asyncio, sys

#自定义库
from inc import springcheck, run, vul, poc, zoom, fofa, hunter, output


# 控制台-参数处理和程序调用
def SpringBoot_Scan_console(args, proxies, header_new):
    handled = False  # 标志变量，用于跟踪是否有命令行参数被处理

    if args.url:
        urlnew = springcheck.check(args.url, proxies, header_new)
        run.url(urlnew, proxies, header_new)
        handled = True

    if args.urlfile:
        asyncio.run(run.file_main(args.urlfile, proxies, header_new))
        handled = True

    if args.vul:
        urlnew = springcheck.check(args.vul, proxies, header_new)
        vul.vul(urlnew, proxies, header_new)
        handled = True

    if args.vulfile:
        poc.poc(args.vulfile, proxies)
        handled = True

    if args.dump:
        urlnew = springcheck.check(args.dump, proxies, header_new)
        run.dump(urlnew, proxies, header_new)
        handled = True

    if args.zoomeye:
        zoom.ZoomDowload(args.zoomeye, proxies)
        handled = True

    if args.fofa:
        fofa.FofaDowload(args.fofa, proxies)
        handled = True

    if args.hunter:
        hunter.HunterDowload(args.hunter, proxies)
        handled = True

    # 如果没有处理任何命令行参数，则调用 output.usage()
    if not handled:
        output.usage()
        sys.exit()








