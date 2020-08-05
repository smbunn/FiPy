## Some example project work with FiPy from PyCom

This is work in progress on a project to learn LoRa, SigFox and NB-IOT (or CAT - M1).

## Project

I plan to use a PySense connected to my FiPy.  Battery powered (2000mAh LiPo) and mounted to my bike
My Android mobile phone posts GPS coordinates to the FiPy using BLE  [Android Link][android] .

The PySense reports humidty, temperature, barometric pressure, ambient light, pitch, yaw and roll.
These are combined with GPS coordinates into a packed Hex payload.

I provide my own gateway for LoRa (I have my own 8-channel packet forwarder  using The THings Network gateway

## Folder structure

The files in the root directory are project specific, plus config files
WiFi setup and the like.  Libraries (operating system or editor specific) templates should go into the
[`lib/`](./lib) directory.

## Contributing guidelines

We’d love for you to help us improve this project. To help us keep this collection
high quality, we request that contributions adhere to the following guidelines.

- **Provide a link to the application or project’s homepage**. Unless it’s
  extremely popular, there’s a chance the maintainers don’t know about or use
  the language, framework, editor, app, or project your change applies to.

- **Provide links to documentation** supporting the change you’re making.
  Current, canonical documentation mentioning the files being ignored is best.
  If documentation isn’t available to support your change, do the best you can
  to explain what the files being ignored are for.

- **Explain why you’re making a change**. Even if it seems self-evident, please
  take a sentence or two to tell us why your change or addition should happen.
  It’s especially helpful to articulate why this change applies to *everyone*
  who works with the applicable technology, rather than just you or your team.

- **Please consider the scope of your change**. If your change is specific to a
  certain language or framework, then make sure the change is made to the
  template for that language or framework, rather than to the template for an
  editor, tool, or operating system.

- **Please only modify *one template* per pull request**. This helps keep pull
  requests and feedback focused on a specific project or technology.

In general, the more you can do to help us understand the change you’re making,
the more likely we’ll be to accept your contribution quickly.


## Contributing workflow

Here’s how we suggest you go about proposing a change to this project:

1. [Fork this project][fork] to your account.
2. [Create a branch][branch] for the change you intend to make.
3. Make your changes to your fork.
4. [Send a pull request][pr] from your fork’s branch to our `master` branch.

Using the web-based interface to make changes is fine too, and will help you
by automatically forking the project and prompting to send a pull request too.

[fork]: https://help.github.com/articles/fork-a-repo/
[branch]: https://help.github.com/articles/creating-and-deleting-branches-within-your-repository
[pr]: https://help.github.com/articles/using-pull-requests/

## License

[CC0-1.0](./LICENSE).
