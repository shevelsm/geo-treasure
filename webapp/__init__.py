import io
import logging

import folium
from flask import Flask, flash, redirect, render_template, request, Response, url_for
from flask_bootstrap import Bootstrap
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_migrate import Migrate
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from webapp.forms import LoginForm, RegistrationForm
from webapp.model import Cluster, db, Point, User, ClusterPoint
from webapp.utils import (
    add_on_click_handler_to_marker,
    create_pie_chart_figure,
    create_popup_and_icon,
)


logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
MAP_START_POSITION = [44.4, 38.75]


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    Bootstrap(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_views = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        radius = request.args.get("radius", 2)
        folium_map = folium.Map(location=MAP_START_POSITION, zoom_start=8)
        with app.app_context():
            query_radius = db.session.query(
                Cluster.id, Cluster.lat, Cluster.long, Point.source,
            ).filter(Cluster.radius == radius)
            query_radius = query_radius.outerjoin(
                ClusterPoint, ClusterPoint.cluster_id == Cluster.id,
            )
            query_radius = query_radius.outerjoin(
                Point, Point.id == ClusterPoint.point_id,
            )
            query_clusters = query_radius.group_by(Cluster.id)
            logging.debug(
                "The number of clusters from the query = {}".format(
                    query_clusters.count()
                )
            )
            for cluster in query_clusters:
                popup, icon = create_popup_and_icon(
                    [row for row in query_radius if row[0] == cluster.id],
                    request.host_url,
                )
                marker = folium.Marker(
                    [cluster.lat, cluster.long], popup=popup, icon=icon,
                ).add_to(folium_map)
                add_on_click_handler_to_marker(
                    folium_map, marker, cluster.id, request.host_url
                )
        return render_template(
            "index.html", folium_map=folium_map._repr_html_(), radius=radius
        )

    @app.route("/clusterajax/<int:cluster_id>")
    def clusterajax(cluster_id):
        points = Point.query.filter(Point.clusters.any(cluster_id=cluster_id))
        return render_template("cluster_points.html", points=points)

    @app.route("/popup.png")
    def popup_png():
        geo_count = request.args.get("geo")
        alter_count = request.args.get("alter")
        auto_count = request.args.get("auto")
        logging.debug(
            "geo {}, alter {}, auto {}".format(geo_count, alter_count, auto_count)
        )
        fig = create_pie_chart_figure(geo_count, alter_count, auto_count)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")

    @app.route("/dev")
    def dev():
        folium_map = folium.Map(location=MAP_START_POSITION, zoom_start=8)
        with app.app_context():
            points_list = Point.query.with_entities(Point.id, Point.lat, Point.long)
            for point in points_list:
                folium.Marker([point[1], point[2]], popup=point[0]).add_to(folium_map)
        return render_template("index.html", folium_map=folium_map._repr_html_())

    @app.route("/login")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        logging.debug("{} has logged in!".format(current_user))
        title = "Authorization"
        login_form = LoginForm()
        return render_template("login.html", page_title=title, form=login_form)

    @app.route("/process_login", methods=["POST"])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash("You've been logged in!")
                return redirect(url_for("index"))
        flash("Incorrect name or password!")
        return redirect(url_for("login"))

    @app.route("/logout")
    def logout():
        logout_user()
        flash("You've been logged out successfully!")
        return redirect(url_for("index"))

    @app.route("/register")
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        title = "Registration"
        registration_form = RegistrationForm()
        return render_template(
            "registration.html", page_title=title, form=registration_form
        )

    @app.route("/process_reg", methods=["POST"])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(
                username=form.username.data, email=form.email.data, role="user"
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(
                        "The error in the field '{}': - {}".format(
                            getattr(form, field).label.text, error
                        )
                    )
        flash("Please, correct errors in the form!")
        return redirect(url_for("user.register"))

    return app
