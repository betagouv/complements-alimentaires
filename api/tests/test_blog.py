from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import BlogPostFactory


class TestBlogApi(APITestCase):
    def test_get_published_blog_posts(self):
        """
        The API should only return published blog posts
        """
        published_blog_posts = [
            BlogPostFactory.create(published=True),
            BlogPostFactory.create(published=True),
        ]
        draft_blog_posts = [
            BlogPostFactory.create(published=False),
            BlogPostFactory.create(published=False),
            BlogPostFactory.create(published=False),
        ]
        response = self.client.get(reverse("api:blog_posts_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body.get("count"), 2)

        results = body.get("results", [])

        for published_blog_post in published_blog_posts:
            self.assertTrue(any(x["id"] == published_blog_post.id for x in results))

        for draft_blog_post in draft_blog_posts:
            self.assertFalse(any(x["id"] == draft_blog_post.id for x in results))

    def test_get_single_blog_post(self):
        """
        The API should return single blog posts if they are published
        """
        published_blog_post = BlogPostFactory.create(published=True)
        draft_blog_post = BlogPostFactory.create(published=False)

        response = self.client.get(reverse("api:single_blog_post", kwargs={"pk": published_blog_post.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse("api:single_blog_post", kwargs={"pk": draft_blog_post.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
