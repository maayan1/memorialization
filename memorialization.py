import argparse
import getpass
import importlib
from typing import Any, Optional, Sequence, Text, Union

from utils.json_storage import reload_data, write_data
from utils.build_posts import create_casualties_posts
from utils.publish_posts import publish_casualties_posts


class Password(argparse.Action):
    """Password argument handler, for making the password typing hidden and safe"""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[Text, Sequence[Any], None],
        option_string: Optional[Text] = None,
    ) -> None:
        values = getpass.getpass()
        setattr(namespace, self.dest, values)


def parse_args() -> argparse.Namespace:
    """Arguments handler"""

    parser = argparse.ArgumentParser(
        prog="Insta Memorialization",
        description="Tool for publishing personal posts describing the war casualties",
    )
    parser.add_argument(
        "-func",
        "--scrap_function_package",
        required=True,
        help="""
            Relative python package path, e.g. "iron_swords.scrap", that includes collect_casualties_data function
       """,
    )
    parser.add_argument(
        "-json",
        "--json_path_package",
        required=True,
        help="""
            Relative python package path, e.g. "iron_swords.paths", that includes JSON_FILE path
        """,
    )
    parser.add_argument("-user", "--instagram_username", required=True)
    parser.add_argument(
        "-pass",
        "--instagram_password",
        action=Password,
        nargs="?",
        dest="instagram_password",
        required=True,
    )
    parser.add_argument(
        "--collect",
        action="store_true",
        help="Collect data about the casualties from the web",
    )
    parser.add_argument(
        "--recollect",
        action="store_true",
        help="Collect data about the casualties from the web, even if it was already collected, unless if it was already published",
    )
    build_arg = parser.add_argument(
        "--build", action="store_true", help="Create and save the posts"
    )
    parser.add_argument(
        "--publish", action="store_true", help="Publish the pre-saved posts"
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Don't publish the post, just make it ready for publishment",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Don't mark post as published, only as tested",
    )
    parser.add_argument(
        "--pages_limit",
        type=int,
        help="Maximal number of pages to collect data from (if not given - all the pages will be scarped)",
    )
    parser.add_argument(
        "--posts_limit",
        type=int,
        help="Maximal number of posts to publish (if not given - all the pages will be published)",
    )
    parser.add_argument(
        "--min_images",
        type=int,
        help="Minimal number of images in a published post. A post with less images won't be published.",
    )
    parser.add_argument(
        "--names", nargs="+", help="Publish posts only for these names", default=[]
    )
    args = parser.parse_args()
    if args.collect and args.publish and not args.build:
        raise argparse.ArgumentError(
            argument=build_arg,
            message='You cannot use "collect" and "publish" without "build"',
        )
    return args


if __name__ == "__main__":
    args = parse_args()

    collect_casualties_data = importlib.import_module(
        args.scrap_function_package
    ).collect_casualties_data
    JSON_FILE = importlib.import_module(args.json_path_package).JSON_FILE

    instagram_username = args.instagram_username
    instagram_password = args.instagram_password

    casualties_data = reload_data(JSON_FILE)

    if args.collect:
        casualties_data = collect_casualties_data(
            casualties_data,
            instagram_username,
            instagram_password,
            args.pages_limit,
            args.recollect,
        )
        write_data(casualties_data, JSON_FILE)

    if args.build:
        casualties_data = create_casualties_posts(casualties_data)
        write_data(casualties_data, JSON_FILE)

    if args.publish:
        casualties_data = publish_casualties_posts(
            casualties_data,
            instagram_username,
            instagram_password,
            args.posts_limit,
            args.min_images,
            args.names,
            args.test,
            args.dry_run,
        )
        write_data(casualties_data, JSON_FILE)
